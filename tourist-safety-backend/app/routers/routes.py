from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import httpx
import math

from app.database import get_db
from app.models.city import City
from app.schemas.route import RouteRequest, RouteResponse, RouteOption, ZoneBreakdown, Coordinates
from app.config import settings

router = APIRouter(prefix="/routes", tags=["Routes"])


async def get_osrm_routes(origin: Coordinates, destination: Coordinates, alternatives: bool = True) -> list[dict]:
    """
    Get routes from OSRM public API.
    Returns multiple route alternatives if available.
    """
    url = f"{settings.OSRM_API_URL}/route/v1/driving/{origin.lng},{origin.lat};{destination.lng},{destination.lat}"
    params = {
        "overview": "full",
        "geometries": "geojson",
        "alternatives": str(alternatives).lower(),
        "steps": "true"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Routing service unavailable")
        
        data = response.json()
        
        if data.get("code") != "Ok":
            raise HTTPException(status_code=400, detail="Could not calculate route")
        
        return data.get("routes", [])


def get_zone_for_point(lat: float, lng: float, cities: list[City]) -> tuple[str, Optional[City]]:
    """
    Determine the safety zone for a point based on nearest city.
    Returns (zone, city) tuple.
    """
    min_distance = float('inf')
    nearest_city = None
    
    for city in cities:
        distance = haversine_distance(lat, lng, city.latitude, city.longitude)
        if distance < min_distance:
            min_distance = distance
            nearest_city = city
    
    # If within 50km of a city, use that city's zone
    # Otherwise, default to orange (unknown)
    if nearest_city and min_distance <= 50:
        return nearest_city.safety_zone, nearest_city
    
    return "orange", None


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in km."""
    R = 6371
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def analyze_route_safety(route_geometry: dict, cities: list[City]) -> tuple[float, ZoneBreakdown, list[dict]]:
    """
    Analyze a route's safety by checking which zones it passes through.
    Returns (safety_score, zone_breakdown, zones_passed)
    """
    coordinates = route_geometry.get("coordinates", [])
    
    if len(coordinates) < 2:
        return 50.0, ZoneBreakdown(
            green_percentage=0, orange_percentage=100, red_percentage=0,
            green_distance_km=0, orange_distance_km=0, red_distance_km=0
        ), []
    
    green_distance = 0.0
    orange_distance = 0.0
    red_distance = 0.0
    zones_passed = []
    current_zone = None
    
    for i in range(1, len(coordinates)):
        prev_coord = coordinates[i-1]
        curr_coord = coordinates[i]
        
        # Calculate segment distance
        segment_distance = haversine_distance(
            prev_coord[1], prev_coord[0],
            curr_coord[1], curr_coord[0]
        )
        
        # Get zone for midpoint of segment
        mid_lat = (prev_coord[1] + curr_coord[1]) / 2
        mid_lng = (prev_coord[0] + curr_coord[0]) / 2
        zone, city = get_zone_for_point(mid_lat, mid_lng, cities)
        
        # Accumulate distance by zone
        if zone == "green":
            green_distance += segment_distance
        elif zone == "orange":
            orange_distance += segment_distance
        else:
            red_distance += segment_distance
        
        # Track zone changes
        if zone != current_zone:
            zones_passed.append({
                "zone": zone,
                "city": city.name if city else "Unknown Area",
                "entry_point": {"lat": prev_coord[1], "lng": prev_coord[0]}
            })
            current_zone = zone
    
    total_distance = green_distance + orange_distance + red_distance
    
    if total_distance == 0:
        total_distance = 0.001  # Avoid division by zero
    
    # Calculate percentages
    zone_breakdown = ZoneBreakdown(
        green_percentage=round((green_distance / total_distance) * 100, 1),
        orange_percentage=round((orange_distance / total_distance) * 100, 1),
        red_percentage=round((red_distance / total_distance) * 100, 1),
        green_distance_km=round(green_distance, 2),
        orange_distance_km=round(orange_distance, 2),
        red_distance_km=round(red_distance, 2)
    )
    
    # Calculate safety score (0-100, higher is safer)
    safety_score = (
        (green_distance * 1.0) +
        (orange_distance * 0.6) +
        (red_distance * 0.2)
    ) / total_distance * 100
    
    return round(safety_score, 1), zone_breakdown, zones_passed


def get_safety_recommendations(zone_breakdown: ZoneBreakdown, zones_passed: list[dict]) -> list[str]:
    """Generate safety recommendations based on route analysis."""
    recommendations = []
    
    if zone_breakdown.red_percentage > 20:
        recommendations.append("⚠️ This route passes through high-risk areas. Consider traveling during daylight hours.")
    
    if zone_breakdown.red_percentage > 0:
        red_cities = [z["city"] for z in zones_passed if z["zone"] == "red"]
        if red_cities:
            recommendations.append(f"🔴 Exercise caution near: {', '.join(set(red_cities))}")
    
    if zone_breakdown.green_percentage > 70:
        recommendations.append("✅ This route primarily passes through safe areas.")
    
    if zone_breakdown.orange_percentage > 50:
        recommendations.append("🟠 Moderate caution advised. Stay on main roads and avoid isolated areas.")
    
    recommendations.append("📱 Keep emergency contacts saved: Police (100), Tourist Helpline (1363)")
    
    return recommendations


def classify_route(safety_score: float) -> str:
    """Classify route based on safety score."""
    if safety_score >= 70:
        return "safe"
    elif safety_score >= 40:
        return "moderate"
    else:
        return "risky"


@router.post("/safe", response_model=RouteResponse)
async def calculate_safe_route(request: RouteRequest, db: Session = Depends(get_db)):
    """
    Calculate the safest route between two points.
    Returns multiple route options with safety analysis.
    """
    # Get all cities for zone calculation
    cities = db.query(City).all()
    
    if not cities:
        raise HTTPException(status_code=500, detail="No city data available for safety analysis")
    
    # Get routes from OSRM
    osrm_routes = await get_osrm_routes(request.origin, request.destination)
    
    route_options = []
    
    for idx, route in enumerate(osrm_routes):
        geometry = route.get("geometry", {})
        distance_m = route.get("distance", 0)
        duration_s = route.get("duration", 0)
        
        # Analyze safety
        safety_score, zone_breakdown, zones_passed = analyze_route_safety(geometry, cities)
        recommendations = get_safety_recommendations(zone_breakdown, zones_passed)
        
        route_option = RouteOption(
            route_id=f"route_{idx + 1}",
            safety_score=safety_score,
            classification=classify_route(safety_score),
            distance_km=round(distance_m / 1000, 2),
            duration_min=round(duration_s / 60, 1),
            geometry=geometry,
            zone_breakdown=zone_breakdown,
            zones_passed=zones_passed,
            recommendations=recommendations
        )
        
        route_options.append(route_option)
    
    # Sort by safety score (highest first)
    route_options.sort(key=lambda x: x.safety_score, reverse=True)
    
    # Find safest and fastest
    safest_route_id = route_options[0].route_id if route_options else ""
    fastest_route_id = min(route_options, key=lambda x: x.duration_min).route_id if route_options else ""
    
    return RouteResponse(
        origin=request.origin,
        destination=request.destination,
        calculated_at=datetime.utcnow().isoformat(),
        routes=route_options,
        safest_route_id=safest_route_id,
        fastest_route_id=fastest_route_id
    )


@router.get("/check-point")
async def check_point_safety(
    lat: float,
    lng: float,
    db: Session = Depends(get_db)
):
    """
    Check the safety zone for a specific point.
    """
    cities = db.query(City).all()
    zone, city = get_zone_for_point(lat, lng, cities)
    
    colors = {"green": "#22c55e", "orange": "#f97316", "red": "#ef4444"}
    
    return {
        "location": {"lat": lat, "lng": lng},
        "safety_zone": zone,
        "safety_color": colors.get(zone, "#6b7280"),
        "nearest_city": city.name if city else None,
        "city_crime_index": city.crime_index if city else None
    }
