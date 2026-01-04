"""
Visualization Router - Chart data and dashboard endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.visualization_service import viz_service

router = APIRouter(prefix="/viz", tags=["Visualization"])


@router.get("/zone-distribution")
async def get_zone_distribution(db: Session = Depends(get_db)):
    """Get city distribution by safety zone (for pie chart)"""
    return viz_service.get_zone_distribution(db)


@router.get("/state-comparison")
async def get_state_comparison(db: Session = Depends(get_db)):
    """Get crime index comparison across states (for bar chart)"""
    return viz_service.get_state_comparison(db)


@router.get("/safest-cities")
async def get_safest_cities(limit: int = 10, db: Session = Depends(get_db)):
    """Get top safest cities (for horizontal bar chart)"""
    return viz_service.get_top_safest_cities(db, limit)


@router.get("/riskiest-cities")
async def get_riskiest_cities(limit: int = 10, db: Session = Depends(get_db)):
    """Get top riskiest cities (for horizontal bar chart)"""
    return viz_service.get_top_riskiest_cities(db, limit)


@router.get("/population-crime")
async def get_population_vs_crime(db: Session = Depends(get_db)):
    """Get population vs crime index (for scatter plot)"""
    return viz_service.get_population_vs_crime(db)


@router.get("/heatmap")
async def get_heatmap_data(db: Session = Depends(get_db)):
    """Get GeoJSON for crime heatmap"""
    return viz_service.get_geojson_heatmap(db)


@router.get("/dashboard")
async def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary statistics"""
    return viz_service.get_dashboard_summary(db)
