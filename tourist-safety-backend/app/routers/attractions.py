from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.database import get_db
from app.models.attraction import Attraction
from app.models.city import City
from app.schemas.attraction import AttractionResponse, AttractionWithCity, AttractionSearchResult
from app.schemas.city import CityWithSafety

router = APIRouter(prefix="/attractions", tags=["Attractions"])


def get_attraction_with_city(attraction: Attraction, city: City) -> AttractionWithCity:
    """Convert attraction to response with city info"""
    return AttractionWithCity(
        id=attraction.id,
        name=attraction.name,
        city_id=attraction.city_id,
        latitude=attraction.latitude,
        longitude=attraction.longitude,
        address=attraction.address,
        category=attraction.category,
        description=attraction.description,
        rating=attraction.rating,
        review_count=attraction.review_count,
        image_url=attraction.image_url,
        opening_hours=attraction.opening_hours,
        entry_fee=attraction.entry_fee,
        best_time_to_visit=attraction.best_time_to_visit,
        popularity_score=attraction.popularity_score,
        city_name=city.name,
        city_state=city.state,
        city_safety_zone=city.safety_zone,
        city_safety_color=CityWithSafety.get_safety_color(city.safety_zone)
    )


@router.get("/search", response_model=AttractionSearchResult)
async def search_attractions(
    q: str = Query(..., min_length=1, description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    safety_zone: Optional[str] = Query(None, description="Filter by city safety zone"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search for tourist attractions by name, city, or category.
    Optionally filter by safety zone.
    """
    query = db.query(Attraction, City).join(City, Attraction.city_id == City.id)
    
    # Search in name, city name, or category
    query = query.filter(
        or_(
            Attraction.name.ilike(f"%{q}%"),
            City.name.ilike(f"%{q}%"),
            Attraction.category.ilike(f"%{q}%")
        )
    )
    
    if category:
        query = query.filter(Attraction.category.ilike(f"%{category}%"))
    
    if safety_zone:
        query = query.filter(City.safety_zone == safety_zone.lower())
    
    # Order by popularity and rating
    query = query.order_by(Attraction.popularity_score.desc(), Attraction.rating.desc())
    
    results = query.limit(limit).all()
    
    attractions = [get_attraction_with_city(attr, city) for attr, city in results]
    
    return AttractionSearchResult(
        query=q,
        total_results=len(attractions),
        attractions=attractions
    )


@router.get("/{attraction_id}", response_model=AttractionWithCity)
async def get_attraction(attraction_id: int, db: Session = Depends(get_db)):
    """Get details for a specific attraction."""
    result = db.query(Attraction, City).join(
        City, Attraction.city_id == City.id
    ).filter(Attraction.id == attraction_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Attraction not found")
    
    attraction, city = result
    return get_attraction_with_city(attraction, city)


@router.get("/city/{city_name}")
async def get_attractions_by_city(
    city_name: str,
    category: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get all attractions in a specific city."""
    city = db.query(City).filter(City.name.ilike(f"%{city_name}%")).first()
    if not city:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found")
    
    query = db.query(Attraction).filter(Attraction.city_id == city.id)
    
    if category:
        query = query.filter(Attraction.category.ilike(f"%{category}%"))
    
    attractions = query.order_by(Attraction.popularity_score.desc()).limit(limit).all()
    
    return {
        "city": {
            "id": city.id,
            "name": city.name,
            "state": city.state,
            "safety_zone": city.safety_zone,
            "safety_color": CityWithSafety.get_safety_color(city.safety_zone)
        },
        "total_attractions": len(attractions),
        "attractions": [get_attraction_with_city(a, city) for a in attractions]
    }


@router.get("/categories/list")
async def get_categories(db: Session = Depends(get_db)):
    """Get list of all attraction categories."""
    categories = db.query(Attraction.category).distinct().all()
    return {
        "categories": [c[0] for c in categories if c[0]]
    }


@router.get("/nearby")
async def get_nearby_attractions(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10, ge=1, le=100),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get attractions near a specific location.
    Uses Haversine formula approximation.
    """
    # Approximate degree per km at this latitude
    lat_diff = radius_km / 111.0
    lng_diff = radius_km / (111.0 * abs(cos_degrees(lat)))
    
    query = db.query(Attraction, City).join(City, Attraction.city_id == City.id)
    query = query.filter(
        Attraction.latitude.between(lat - lat_diff, lat + lat_diff),
        Attraction.longitude.between(lng - lng_diff, lng + lng_diff)
    )
    
    results = query.limit(limit).all()
    
    # Calculate actual distances and sort
    attractions_with_distance = []
    for attraction, city in results:
        distance = haversine_distance(lat, lng, attraction.latitude, attraction.longitude)
        if distance <= radius_km:
            attr_data = get_attraction_with_city(attraction, city).model_dump()
            attr_data["distance_km"] = round(distance, 2)
            attractions_with_distance.append(attr_data)
    
    # Sort by distance
    attractions_with_distance.sort(key=lambda x: x["distance_km"])
    
    return {
        "center": {"lat": lat, "lng": lng},
        "radius_km": radius_km,
        "count": len(attractions_with_distance),
        "attractions": attractions_with_distance
    }


def cos_degrees(degrees: float) -> float:
    """Cosine of angle in degrees."""
    import math
    return math.cos(math.radians(degrees))


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in km."""
    import math
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c
