from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.city import City
from app.models.crime_statistic import CrimeStatistic
from app.schemas.city import CityResponse, CityWithSafety, CitySafetyOverview

router = APIRouter(prefix="/safety", tags=["Safety"])


def get_safety_details(city: City) -> CityWithSafety:
    """Convert city to CityWithSafety response"""
    return CityWithSafety(
        id=city.id,
        name=city.name,
        state=city.state,
        latitude=city.latitude,
        longitude=city.longitude,
        population=city.population,
        crime_index=city.crime_index,
        safety_zone=city.safety_zone,
        safety_color=CityWithSafety.get_safety_color(city.safety_zone),
        safety_description=CityWithSafety.get_safety_description(city.safety_zone)
    )


@router.get("/cities", response_model=CitySafetyOverview)
async def get_all_cities_safety(
    db: Session = Depends(get_db),
    zone: Optional[str] = Query(None, description="Filter by safety zone: green, orange, red"),
    state: Optional[str] = Query(None, description="Filter by state")
):
    """
    Get safety overview of all cities.
    Optionally filter by safety zone or state.
    """
    query = db.query(City)
    
    if zone:
        query = query.filter(City.safety_zone == zone.lower())
    if state:
        query = query.filter(City.state.ilike(f"%{state}%"))
    
    cities = query.order_by(City.crime_index.asc()).all()
    
    # Count by zone
    all_cities = db.query(City).all()
    green_count = sum(1 for c in all_cities if c.safety_zone == "green")
    orange_count = sum(1 for c in all_cities if c.safety_zone == "orange")
    red_count = sum(1 for c in all_cities if c.safety_zone == "red")
    
    return CitySafetyOverview(
        total_cities=len(all_cities),
        green_count=green_count,
        orange_count=orange_count,
        red_count=red_count,
        cities=[get_safety_details(city) for city in cities]
    )


@router.get("/city/{city_name}", response_model=CityWithSafety)
async def get_city_safety(city_name: str, db: Session = Depends(get_db)):
    """
    Get detailed safety information for a specific city.
    """
    city = db.query(City).filter(City.name.ilike(f"%{city_name}%")).first()
    if not city:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found")
    
    return get_safety_details(city)


@router.get("/zones/geojson")
async def get_safety_zones_geojson(db: Session = Depends(get_db)):
    """
    Get all cities as GeoJSON for map visualization.
    Each city is a point with safety zone properties.
    """
    cities = db.query(City).all()
    
    features = []
    for city in cities:
        feature = {
            "type": "Feature",
            "properties": {
                "id": city.id,
                "name": city.name,
                "state": city.state,
                "safety_zone": city.safety_zone,
                "crime_index": city.crime_index,
                "population": city.population,
                "color": CityWithSafety.get_safety_color(city.safety_zone)
            },
            "geometry": {
                "type": "Point",
                "coordinates": [city.longitude, city.latitude]
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


@router.get("/ranking")
async def get_safety_ranking(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    order: str = Query("safest", description="Order: 'safest' or 'riskiest'")
):
    """
    Get cities ranked by safety.
    """
    query = db.query(City)
    
    if order == "safest":
        query = query.order_by(City.crime_index.asc())
    else:
        query = query.order_by(City.crime_index.desc())
    
    cities = query.limit(limit).all()
    
    return {
        "order": order,
        "count": len(cities),
        "cities": [
            {
                "rank": idx + 1,
                **get_safety_details(city).model_dump()
            }
            for idx, city in enumerate(cities)
        ]
    }


@router.get("/states")
async def get_states_safety_summary(db: Session = Depends(get_db)):
    """
    Get safety summary aggregated by state.
    """
    cities = db.query(City).all()
    
    # Aggregate by state
    state_data = {}
    for city in cities:
        if city.state not in state_data:
            state_data[city.state] = {
                "state": city.state,
                "cities": [],
                "total_crime_index": 0,
                "city_count": 0
            }
        state_data[city.state]["cities"].append(city.name)
        state_data[city.state]["total_crime_index"] += city.crime_index
        state_data[city.state]["city_count"] += 1
    
    # Calculate average and determine zone
    result = []
    for state, data in state_data.items():
        avg_crime_index = data["total_crime_index"] / data["city_count"]
        
        if avg_crime_index <= 30:
            zone = "green"
        elif avg_crime_index <= 60:
            zone = "orange"
        else:
            zone = "red"
        
        result.append({
            "state": state,
            "city_count": data["city_count"],
            "average_crime_index": round(avg_crime_index, 2),
            "safety_zone": zone,
            "safety_color": CityWithSafety.get_safety_color(zone),
            "cities": data["cities"]
        })
    
    # Sort by average crime index
    result.sort(key=lambda x: x["average_crime_index"])
    
    return {"states": result}
