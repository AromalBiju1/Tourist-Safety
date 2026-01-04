"""
Analytics Router - ML-powered safety analytics endpoints
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.models.city import City
from app.services.ml_service import safety_ml_service
from app.services.crime_service import crime_service

router = APIRouter(prefix="/analytics", tags=["Analytics & ML"])


@router.get("/predict-safety/{city_name}")
async def predict_city_safety(
    city_name: str,
    db: Session = Depends(get_db)
):
    """
    Get ML-powered safety prediction for a city.
    Includes risk level, confidence score, and recommendations.
    """
    city = db.query(City).filter(City.name.ilike(f"%{city_name}%")).first()
    
    if not city:
        return {"error": f"City '{city_name}' not found"}
    
    # Get crime trend for better prediction
    trend = crime_service.get_crime_trend(db, city.id)
    trend_data = [d["crime_index"] for d in trend.get("yearly_data", [])]
    
    # Get prediction
    prediction = safety_ml_service.predict_safety(
        crime_index=city.crime_index,
        crime_trends=trend_data if trend_data else None
    )
    
    return {
        "city": {
            "id": city.id,
            "name": city.name,
            "state": city.state,
            "crime_index": city.crime_index,
            "safety_zone": city.safety_zone
        },
        "prediction": {
            "risk_level": prediction.risk_level.value,
            "confidence": prediction.confidence,
            "factors": prediction.factors,
            "recommendations": prediction.recommendations
        },
        "trend": trend
    }


@router.get("/compare-cities")
async def compare_cities(
    cities: str = Query(..., description="Comma-separated city names"),
    db: Session = Depends(get_db)
):
    """
    Compare safety metrics across multiple cities.
    """
    city_names = [c.strip() for c in cities.split(",")]
    
    # Find cities
    found_cities = []
    for name in city_names:
        city = db.query(City).filter(City.name.ilike(f"%{name}%")).first()
        if city:
            found_cities.append(city.id)
    
    if not found_cities:
        return {"error": "No cities found"}
    
    comparison = crime_service.get_city_comparison(db, found_cities)
    
    return {
        "compared_cities": len(comparison),
        "cities": comparison
    }


@router.get("/state-summary")
async def get_state_summary(db: Session = Depends(get_db)):
    """
    Get aggregated safety summary by state.
    """
    summaries = crime_service.get_state_summary(db)
    
    return {
        "total_states": len(summaries),
        "safest_state": summaries[0] if summaries else None,
        "riskiest_state": summaries[-1] if summaries else None,
        "states": summaries
    }


@router.get("/hotspots")
async def get_safety_hotspots(
    zone: str = Query("red", description="Zone type: 'red' for dangerous, 'green' for safest"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get safety hotspots - most dangerous or safest cities.
    """
    hotspots = crime_service.get_hotspots(db, limit=limit, zone_type=zone)
    
    return {
        "zone_type": zone,
        "count": len(hotspots),
        "hotspots": hotspots
    }


@router.get("/crime-trend/{city_name}")
async def get_crime_trend(
    city_name: str,
    years: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Get crime trend analysis for a city over specified years.
    """
    city = db.query(City).filter(City.name.ilike(f"%{city_name}%")).first()
    
    if not city:
        return {"error": f"City '{city_name}' not found"}
    
    trend = crime_service.get_crime_trend(db, city.id, years=years)
    
    return {
        "city": city.name,
        "state": city.state,
        "current_index": city.crime_index,
        "current_zone": city.safety_zone,
        "trend_analysis": trend
    }


@router.get("/safety-score")
async def calculate_safety_score(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    db: Session = Depends(get_db)
):
    """
    Calculate safety score for a specific location.
    Uses nearest city data for scoring.
    """
    cities = db.query(City).all()
    
    # Find nearest city
    min_distance = float('inf')
    nearest_city = None
    
    import math
    
    for city in cities:
        # Haversine distance
        R = 6371
        lat1_rad = math.radians(lat)
        lat2_rad = math.radians(city.latitude)
        delta_lat = math.radians(city.latitude - lat)
        delta_lon = math.radians(city.longitude - lng)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        if distance < min_distance:
            min_distance = distance
            nearest_city = city
    
    if not nearest_city:
        return {"error": "No city data available"}
    
    # Adjust score based on distance
    # Farther from city center = more uncertainty
    distance_factor = min(1.0, 50 / min_distance) if min_distance > 0 else 1.0
    
    prediction = safety_ml_service.predict_safety(nearest_city.crime_index)
    adjusted_confidence = prediction.confidence * distance_factor
    
    return {
        "location": {"lat": lat, "lng": lng},
        "nearest_city": {
            "name": nearest_city.name,
            "state": nearest_city.state,
            "distance_km": round(min_distance, 2)
        },
        "safety_zone": nearest_city.safety_zone,
        "crime_index": nearest_city.crime_index,
        "risk_level": prediction.risk_level.value,
        "confidence": round(adjusted_confidence, 2),
        "note": "Score based on nearest city data" if min_distance > 10 else "Location within city limits"
    }


@router.get("/recommendations/{city_name}")
async def get_travel_recommendations(
    city_name: str,
    db: Session = Depends(get_db)
):
    """
    Get personalized travel recommendations for a city.
    """
    city = db.query(City).filter(City.name.ilike(f"%{city_name}%")).first()
    
    if not city:
        return {"error": f"City '{city_name}' not found"}
    
    prediction = safety_ml_service.predict_safety(city.crime_index)
    
    # Get nearby safer alternatives if this is a high-risk city
    alternatives = []
    if city.safety_zone == "red":
        safer_cities = db.query(City).filter(
            City.state == city.state,
            City.safety_zone.in_(["green", "orange"]),
            City.id != city.id
        ).order_by(City.crime_index.asc()).limit(3).all()
        
        alternatives = [
            {
                "name": c.name,
                "safety_zone": c.safety_zone,
                "crime_index": c.crime_index
            }
            for c in safer_cities
        ]
    
    return {
        "city": {
            "name": city.name,
            "state": city.state,
            "safety_zone": city.safety_zone,
            "crime_index": city.crime_index
        },
        "risk_level": prediction.risk_level.value,
        "recommendations": prediction.recommendations,
        "factors": prediction.factors,
        "safer_alternatives": alternatives,
        "emergency_numbers": {
            "police": "100",
            "ambulance": "102",
            "women_helpline": "1091",
            "tourist_helpline": "1363"
        }
    }


@router.post("/recalculate-indices")
async def recalculate_all_indices(db: Session = Depends(get_db)):
    """
    Recalculate crime indices for all cities.
    Use after adding new crime data.
    """
    result = crime_service.update_all_city_indices(db)
    
    return {
        "message": "Crime indices recalculated",
        "zone_counts": result
    }
