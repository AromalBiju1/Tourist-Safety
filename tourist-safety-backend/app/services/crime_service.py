"""
Crime Analysis Service
Handles crime data processing, analysis, and statistics generation
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.city import City
from app.models.crime_statistic import CrimeStatistic
from app.services.ml_service import safety_ml_service


class CrimeAnalysisService:
    """
    Service for analyzing crime data and generating insights
    """
    
    def calculate_city_crime_index(
        self,
        db: Session,
        city_id: int,
        year: Optional[int] = None
    ) -> Optional[float]:
        """
        Calculate or update crime index for a city
        
        Args:
            db: Database session
            city_id: City ID
            year: Optional specific year (defaults to latest)
        
        Returns:
            Calculated crime index or None
        """
        city = db.query(City).filter(City.id == city_id).first()
        if not city:
            return None
        
        # Get latest crime statistics
        query = db.query(CrimeStatistic).filter(CrimeStatistic.city_id == city_id)
        if year:
            query = query.filter(CrimeStatistic.year == year)
        else:
            query = query.order_by(CrimeStatistic.year.desc())
        
        crime_stat = query.first()
        
        if not crime_stat:
            return city.crime_index  # Return existing if no stats
        
        # Calculate using ML service
        crime_index = safety_ml_service.calculate_crime_index(
            murder=crime_stat.murder,
            robbery=crime_stat.robbery,
            kidnapping=crime_stat.kidnapping,
            riots=crime_stat.riots,
            burglary=crime_stat.burglary,
            theft=crime_stat.theft,
            crimes_against_women=crime_stat.crimes_against_women,
            cyber_crimes=crime_stat.cyber_crimes,
            population=city.population or 1000000
        )
        
        return crime_index
    
    def update_all_city_indices(self, db: Session) -> Dict[str, int]:
        """
        Recalculate crime indices for all cities
        
        Returns:
            Dict with counts of updated cities by zone
        """
        cities = db.query(City).all()
        zone_counts = {"green": 0, "orange": 0, "red": 0}
        
        for city in cities:
            crime_index = self.calculate_city_crime_index(db, city.id)
            
            if crime_index is not None:
                city.crime_index = crime_index
                city.safety_zone = safety_ml_service.classify_safety_zone(crime_index)
                zone_counts[city.safety_zone] += 1
        
        db.commit()
        return zone_counts
    
    def get_crime_trend(
        self,
        db: Session,
        city_id: int,
        years: int = 5
    ) -> Dict:
        """
        Get crime trend for a city over specified years
        
        Args:
            db: Database session
            city_id: City ID
            years: Number of years to analyze
        
        Returns:
            Dict with trend analysis
        """
        current_year = datetime.now().year
        
        stats = db.query(CrimeStatistic).filter(
            CrimeStatistic.city_id == city_id,
            CrimeStatistic.year >= current_year - years
        ).order_by(CrimeStatistic.year).all()
        
        if not stats:
            return {"trend": "no_data", "data": []}
        
        city = db.query(City).filter(City.id == city_id).first()
        population = city.population if city else 1000000
        
        historical_data = []
        for stat in stats:
            index = safety_ml_service.calculate_crime_index(
                murder=stat.murder,
                robbery=stat.robbery,
                kidnapping=stat.kidnapping,
                riots=stat.riots,
                burglary=stat.burglary,
                theft=stat.theft,
                crimes_against_women=stat.crimes_against_women,
                cyber_crimes=stat.cyber_crimes,
                population=population
            )
            historical_data.append((stat.year, index))
        
        trend_analysis = safety_ml_service.analyze_crime_trend(historical_data)
        trend_analysis["yearly_data"] = [
            {"year": year, "crime_index": index}
            for year, index in historical_data
        ]
        
        return trend_analysis
    
    def get_city_comparison(
        self,
        db: Session,
        city_ids: List[int]
    ) -> List[Dict]:
        """
        Compare safety metrics across multiple cities
        
        Args:
            db: Database session
            city_ids: List of city IDs to compare
        
        Returns:
            List of city comparison data
        """
        cities = db.query(City).filter(City.id.in_(city_ids)).all()
        
        comparison = []
        for city in cities:
            prediction = safety_ml_service.predict_safety(city.crime_index)
            
            comparison.append({
                "id": city.id,
                "name": city.name,
                "state": city.state,
                "crime_index": city.crime_index,
                "safety_zone": city.safety_zone,
                "risk_level": prediction.risk_level.value,
                "confidence": prediction.confidence,
                "population": city.population,
                "factors": prediction.factors,
                "recommendations": prediction.recommendations
            })
        
        # Sort by crime index (safest first)
        comparison.sort(key=lambda x: x["crime_index"])
        
        return comparison
    
    def get_state_summary(self, db: Session) -> List[Dict]:
        """
        Get aggregated safety summary by state
        
        Returns:
            List of state summaries
        """
        # Aggregate by state
        state_data = db.query(
            City.state,
            func.count(City.id).label("city_count"),
            func.avg(City.crime_index).label("avg_crime_index"),
            func.sum(City.population).label("total_population")
        ).group_by(City.state).all()
        
        summaries = []
        for state, city_count, avg_index, total_pop in state_data:
            zone = safety_ml_service.classify_safety_zone(avg_index)
            
            summaries.append({
                "state": state,
                "city_count": city_count,
                "average_crime_index": round(avg_index, 2),
                "safety_zone": zone,
                "total_population": total_pop,
                "safety_color": self._get_zone_color(zone)
            })
        
        # Sort by average crime index
        summaries.sort(key=lambda x: x["average_crime_index"])
        
        return summaries
    
    def get_hotspots(
        self,
        db: Session,
        limit: int = 10,
        zone_type: str = "red"
    ) -> List[Dict]:
        """
        Get safety hotspots (most dangerous or safest areas)
        
        Args:
            db: Database session
            limit: Number of cities to return
            zone_type: "red" for dangerous, "green" for safest
        
        Returns:
            List of hotspot cities
        """
        query = db.query(City).filter(City.safety_zone == zone_type)
        
        if zone_type == "red":
            query = query.order_by(City.crime_index.desc())
        else:
            query = query.order_by(City.crime_index.asc())
        
        cities = query.limit(limit).all()
        
        return [
            {
                "id": city.id,
                "name": city.name,
                "state": city.state,
                "crime_index": city.crime_index,
                "safety_zone": city.safety_zone,
                "latitude": city.latitude,
                "longitude": city.longitude,
                "population": city.population
            }
            for city in cities
        ]
    
    def _get_zone_color(self, zone: str) -> str:
        """Get hex color for safety zone"""
        colors = {
            "green": "#22c55e",
            "orange": "#f97316",
            "red": "#ef4444"
        }
        return colors.get(zone, "#6b7280")


# Singleton instance
crime_service = CrimeAnalysisService()
