"""
Data Visualization Service
Generates charts and statistics for the frontend
"""
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
import json

from app.models.city import City
from app.models.crime_statistic import CrimeStatistic


class VisualizationService:
    """
    Service for generating data visualizations and statistics
    """
    
    def get_zone_distribution(self, db: Session) -> Dict:
        """
        Get distribution of cities by safety zone
        Returns data suitable for pie/donut chart
        """
        zones = db.query(
            City.safety_zone,
            func.count(City.id).label('count')
        ).group_by(City.safety_zone).all()
        
        colors = {
            "green": "#22c55e",
            "orange": "#f97316",
            "red": "#ef4444"
        }
        
        labels = {
            "green": "Safe",
            "orange": "Moderate Risk",
            "red": "High Risk"
        }
        
        data = []
        for zone, count in zones:
            data.append({
                "zone": zone,
                "label": labels.get(zone, zone),
                "count": count,
                "color": colors.get(zone, "#gray")
            })
        
        return {
            "type": "pie",
            "title": "Cities by Safety Zone",
            "data": data
        }
    
    def get_state_comparison(self, db: Session) -> Dict:
        """
        Get crime index comparison across states
        Returns data suitable for bar chart
        """
        states = db.query(
            City.state,
            func.avg(City.crime_index).label('avg_index'),
            func.count(City.id).label('city_count')
        ).group_by(City.state).order_by(func.avg(City.crime_index)).all()
        
        data = []
        for state, avg_index, count in states:
            # Determine color based on average
            if avg_index <= 30:
                color = "#22c55e"
            elif avg_index <= 60:
                color = "#f97316"
            else:
                color = "#ef4444"
            
            data.append({
                "state": state,
                "average_crime_index": round(avg_index, 2),
                "city_count": count,
                "color": color
            })
        
        return {
            "type": "bar",
            "title": "Average Crime Index by State",
            "x_axis": "State",
            "y_axis": "Crime Index",
            "data": data
        }
    
    def get_top_safest_cities(self, db: Session, limit: int = 10) -> Dict:
        """
        Get top safest cities
        Returns data suitable for horizontal bar chart
        """
        cities = db.query(City).order_by(City.crime_index.asc()).limit(limit).all()
        
        data = []
        for city in cities:
            data.append({
                "name": city.name,
                "state": city.state,
                "crime_index": city.crime_index,
                "color": "#22c55e"
            })
        
        return {
            "type": "horizontal_bar",
            "title": f"Top {limit} Safest Cities",
            "data": data
        }
    
    def get_top_riskiest_cities(self, db: Session, limit: int = 10) -> Dict:
        """
        Get top riskiest cities
        """
        cities = db.query(City).order_by(City.crime_index.desc()).limit(limit).all()
        
        data = []
        for city in cities:
            data.append({
                "name": city.name,
                "state": city.state,
                "crime_index": city.crime_index,
                "color": "#ef4444"
            })
        
        return {
            "type": "horizontal_bar",
            "title": f"Top {limit} Highest Risk Cities",
            "data": data
        }
    
    def get_population_vs_crime(self, db: Session) -> Dict:
        """
        Get population vs crime index scatter plot data
        """
        cities = db.query(City).filter(City.population > 0).all()
        
        data = []
        for city in cities:
            colors = {
                "green": "#22c55e",
                "orange": "#f97316",
                "red": "#ef4444"
            }
            
            data.append({
                "name": city.name,
                "x": city.population / 1000000,  # Convert to millions
                "y": city.crime_index,
                "zone": city.safety_zone,
                "color": colors.get(city.safety_zone, "#gray")
            })
        
        return {
            "type": "scatter",
            "title": "Population vs Crime Index",
            "x_axis": "Population (Millions)",
            "y_axis": "Crime Index",
            "data": data
        }
    
    def get_geojson_heatmap(self, db: Session) -> Dict:
        """
        Get GeoJSON with crime intensity for heatmap
        """
        cities = db.query(City).all()
        
        features = []
        for city in cities:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [city.longitude, city.latitude]
                },
                "properties": {
                    "name": city.name,
                    "state": city.state,
                    "crime_index": city.crime_index,
                    "safety_zone": city.safety_zone,
                    "population": city.population,
                    # Intensity for heatmap (0-1)
                    "intensity": city.crime_index / 100
                }
            }
            features.append(feature)
        
        return {
            "type": "FeatureCollection",
            "features": features
        }
    
    def get_dashboard_summary(self, db: Session) -> Dict:
        """
        Get summary statistics for dashboard
        """
        total_cities = db.query(City).count()
        
        zone_counts = {}
        for zone in ["green", "orange", "red"]:
            zone_counts[zone] = db.query(City).filter(City.safety_zone == zone).count()
        
        avg_crime_index = db.query(func.avg(City.crime_index)).scalar()
        
        safest = db.query(City).order_by(City.crime_index.asc()).first()
        riskiest = db.query(City).order_by(City.crime_index.desc()).first()
        
        return {
            "total_cities": total_cities,
            "zone_distribution": zone_counts,
            "average_crime_index": round(avg_crime_index, 2) if avg_crime_index else 0,
            "safest_city": {
                "name": safest.name,
                "state": safest.state,
                "crime_index": safest.crime_index
            } if safest else None,
            "riskiest_city": {
                "name": riskiest.name,
                "state": riskiest.state,
                "crime_index": riskiest.crime_index
            } if riskiest else None,
            "safety_score_india": round(100 - (avg_crime_index or 50), 1)
        }


# Singleton instance
viz_service = VisualizationService()
