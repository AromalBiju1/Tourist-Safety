"""
Routing Service with Safety-Aware Path Finding
Integrates with OSRM for route calculation and applies safety scoring
"""
import httpx
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from app.config import settings


@dataclass
class RouteSegment:
    """A segment of a route with safety information"""
    start_coords: Tuple[float, float]  # (lat, lng)
    end_coords: Tuple[float, float]
    distance_km: float
    duration_min: float
    safety_zone: str
    city_name: Optional[str]


@dataclass
class SafeRoute:
    """A complete route with safety analysis"""
    route_id: str
    total_distance_km: float
    total_duration_min: float
    safety_score: float
    classification: str
    geometry: Dict
    segments: List[RouteSegment]
    zone_breakdown: Dict[str, float]
    recommendations: List[str]


class RoutingService:
    """
    Service for calculating safe routes using OSRM
    """
    
    def __init__(self, osrm_url: str = None):
        self.osrm_url = osrm_url or settings.OSRM_API_URL
    
    async def get_routes(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        alternatives: bool = True
    ) -> List[Dict]:
        """
        Get routes from OSRM
        
        Args:
            origin: (lat, lng) tuple
            destination: (lat, lng) tuple
            alternatives: Whether to get alternative routes
        
        Returns:
            List of route dictionaries from OSRM
        """
        # OSRM expects lng,lat order
        url = f"{self.osrm_url}/route/v1/driving/{origin[1]},{origin[0]};{destination[1]},{destination[0]}"
        
        params = {
            "overview": "full",
            "geometries": "geojson",
            "alternatives": str(alternatives).lower(),
            "steps": "true",
            "annotations": "true"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("code") != "Ok":
                    return []
                
                return data.get("routes", [])
                
            except httpx.RequestError as e:
                print(f"OSRM request failed: {e}")
                return []
    
    def analyze_route_safety(
        self,
        route: Dict,
        cities: List[Dict]
    ) -> Tuple[float, Dict[str, float], List[Dict]]:
        """
        Analyze a route's safety by checking zones it passes through
        
        Args:
            route: OSRM route dictionary
            cities: List of city dicts with lat, lng, safety_zone
        
        Returns:
            Tuple of (safety_score, zone_breakdown, zones_passed)
        """
        geometry = route.get("geometry", {})
        coordinates = geometry.get("coordinates", [])
        
        if len(coordinates) < 2:
            return 50.0, {"green": 0, "orange": 100, "red": 0}, []
        
        green_distance = 0.0
        orange_distance = 0.0
        red_distance = 0.0
        zones_passed = []
        current_zone = None
        
        for i in range(1, len(coordinates)):
            prev_coord = coordinates[i-1]
            curr_coord = coordinates[i]
            
            # Calculate segment distance
            segment_distance = self._haversine_distance(
                prev_coord[1], prev_coord[0],  # lat, lng from lng,lat
                curr_coord[1], curr_coord[0]
            )
            
            # Get zone for midpoint
            mid_lat = (prev_coord[1] + curr_coord[1]) / 2
            mid_lng = (prev_coord[0] + curr_coord[0]) / 2
            zone, city = self._get_zone_for_point(mid_lat, mid_lng, cities)
            
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
                    "city": city.get("name") if city else "Unknown Area",
                    "entry_point": {"lat": prev_coord[1], "lng": prev_coord[0]}
                })
                current_zone = zone
        
        total_distance = green_distance + orange_distance + red_distance
        
        if total_distance == 0:
            total_distance = 0.001
        
        # Calculate breakdown percentages
        zone_breakdown = {
            "green_percentage": round((green_distance / total_distance) * 100, 1),
            "orange_percentage": round((orange_distance / total_distance) * 100, 1),
            "red_percentage": round((red_distance / total_distance) * 100, 1),
            "green_distance_km": round(green_distance, 2),
            "orange_distance_km": round(orange_distance, 2),
            "red_distance_km": round(red_distance, 2)
        }
        
        # Calculate safety score (0-100, higher is safer)
        safety_score = (
            (green_distance * 1.0) +
            (orange_distance * 0.6) +
            (red_distance * 0.2)
        ) / total_distance * 100
        
        return round(safety_score, 1), zone_breakdown, zones_passed
    
    def _get_zone_for_point(
        self,
        lat: float,
        lng: float,
        cities: List[Dict]
    ) -> Tuple[str, Optional[Dict]]:
        """Get the safety zone for a point based on nearest city"""
        min_distance = float('inf')
        nearest_city = None
        
        for city in cities:
            distance = self._haversine_distance(
                lat, lng,
                city["latitude"], city["longitude"]
            )
            if distance < min_distance:
                min_distance = distance
                nearest_city = city
        
        # If within 50km of a city, use that city's zone
        if nearest_city and min_distance <= 50:
            return nearest_city.get("safety_zone", "orange"), nearest_city
        
        return "orange", None
    
    def _haversine_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """Calculate distance between two points in km"""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2)**2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def get_safety_recommendations(
        self,
        zone_breakdown: Dict,
        zones_passed: List[Dict]
    ) -> List[str]:
        """Generate safety recommendations for a route"""
        recommendations = []
        
        red_pct = zone_breakdown.get("red_percentage", 0)
        green_pct = zone_breakdown.get("green_percentage", 0)
        orange_pct = zone_breakdown.get("orange_percentage", 0)
        
        if red_pct > 20:
            recommendations.append("⚠️ This route passes through high-risk areas. Consider traveling during daylight hours.")
        
        if red_pct > 0:
            red_cities = [z["city"] for z in zones_passed if z["zone"] == "red"]
            if red_cities:
                unique_cities = list(set(red_cities))[:3]  # Limit to 3
                recommendations.append(f"🔴 Exercise caution near: {', '.join(unique_cities)}")
        
        if green_pct > 70:
            recommendations.append("✅ This route primarily passes through safe areas.")
        
        if orange_pct > 50:
            recommendations.append("🟠 Moderate caution advised. Stay on main roads and avoid isolated areas.")
        
        recommendations.append("📱 Keep emergency contacts saved: Police (100), Tourist Helpline (1363)")
        
        if red_pct > 30:
            recommendations.append("👥 Consider traveling with others for added safety.")
        
        return recommendations
    
    def classify_route(self, safety_score: float) -> str:
        """Classify a route based on its safety score"""
        if safety_score >= 70:
            return "safe"
        elif safety_score >= 40:
            return "moderate"
        else:
            return "risky"


# Singleton instance
routing_service = RoutingService()
