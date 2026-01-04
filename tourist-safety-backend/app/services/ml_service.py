"""
Machine Learning Service for Safety Analysis
Uses clustering and scoring algorithms to analyze crime patterns
"""
import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SafetyPrediction:
    """Result of safety prediction for a location"""
    risk_level: RiskLevel
    confidence: float
    crime_index: float
    factors: List[str]
    recommendations: List[str]


@dataclass
class CrimeWeights:
    """Weights for different crime categories in safety scoring"""
    murder: float = 10.0
    robbery: float = 5.0
    kidnapping: float = 7.0
    riots: float = 3.0
    burglary: float = 2.0
    theft: float = 1.0
    crimes_against_women: float = 8.0
    cyber_crimes: float = 1.5


class SafetyMLService:
    """
    Machine Learning service for safety analysis and predictions
    """
    
    def __init__(self):
        self.weights = CrimeWeights()
        # Normalization factors based on national averages
        self.national_avg_crime_rate = 350.0  # per 100k population
        
    def calculate_crime_index(
        self,
        murder: int,
        robbery: int,
        kidnapping: int,
        riots: int,
        burglary: int,
        theft: int,
        crimes_against_women: int,
        cyber_crimes: int,
        population: int
    ) -> float:
        """
        Calculate normalized crime index (0-100) using weighted formula
        """
        if population <= 0:
            return 50.0  # Default for unknown population
        
        # Calculate weighted crime score
        weighted_score = (
            murder * self.weights.murder +
            robbery * self.weights.robbery +
            kidnapping * self.weights.kidnapping +
            riots * self.weights.riots +
            burglary * self.weights.burglary +
            theft * self.weights.theft +
            crimes_against_women * self.weights.crimes_against_women +
            cyber_crimes * self.weights.cyber_crimes
        )
        
        # Normalize per 100,000 population
        crime_rate = (weighted_score / population) * 100000
        
        # Convert to 0-100 index using sigmoid-like normalization
        # This ensures most values fall in a reasonable range
        normalized_index = 100 * (1 - np.exp(-crime_rate / self.national_avg_crime_rate))
        
        return round(min(max(normalized_index, 0), 100), 2)
    
    def classify_safety_zone(self, crime_index: float) -> str:
        """
        Classify a location into safety zones based on crime index
        Uses threshold-based classification
        """
        if crime_index <= 30:
            return "green"
        elif crime_index <= 60:
            return "orange"
        else:
            return "red"
    
    def predict_safety(
        self,
        crime_index: float,
        crime_trends: Optional[List[float]] = None,
        nearby_zones: Optional[List[str]] = None
    ) -> SafetyPrediction:
        """
        Predict safety level with confidence score and recommendations
        """
        # Base risk level from crime index
        if crime_index <= 20:
            risk_level = RiskLevel.LOW
            base_confidence = 0.9
        elif crime_index <= 40:
            risk_level = RiskLevel.LOW
            base_confidence = 0.75
        elif crime_index <= 55:
            risk_level = RiskLevel.MODERATE
            base_confidence = 0.8
        elif crime_index <= 70:
            risk_level = RiskLevel.MODERATE
            base_confidence = 0.7
        elif crime_index <= 85:
            risk_level = RiskLevel.HIGH
            base_confidence = 0.8
        else:
            risk_level = RiskLevel.CRITICAL
            base_confidence = 0.9
        
        # Adjust confidence based on trend consistency
        if crime_trends and len(crime_trends) >= 3:
            trend_variance = np.var(crime_trends)
            if trend_variance < 10:
                base_confidence = min(base_confidence + 0.05, 0.95)
            elif trend_variance > 50:
                base_confidence = max(base_confidence - 0.1, 0.5)
        
        # Generate factors
        factors = self._identify_risk_factors(crime_index, crime_trends)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_level, factors)
        
        return SafetyPrediction(
            risk_level=risk_level,
            confidence=round(base_confidence, 2),
            crime_index=crime_index,
            factors=factors,
            recommendations=recommendations
        )
    
    def _identify_risk_factors(
        self,
        crime_index: float,
        trends: Optional[List[float]] = None
    ) -> List[str]:
        """Identify contributing risk factors"""
        factors = []
        
        if crime_index > 70:
            factors.append("High overall crime rate")
        elif crime_index > 50:
            factors.append("Elevated crime rate")
        
        if trends and len(trends) >= 2:
            recent_trend = trends[-1] - trends[-2]
            if recent_trend > 5:
                factors.append("Rising crime trend")
            elif recent_trend < -5:
                factors.append("Declining crime trend (positive)")
        
        if crime_index > 60:
            factors.append("Tourist areas may require extra caution")
        
        return factors if factors else ["No significant risk factors identified"]
    
    def _generate_recommendations(
        self,
        risk_level: RiskLevel,
        factors: List[str]
    ) -> List[str]:
        """Generate safety recommendations based on risk level"""
        recommendations = []
        
        if risk_level == RiskLevel.LOW:
            recommendations = [
                "✅ Generally safe for tourists",
                "📱 Keep emergency contacts saved",
                "🚶 Enjoy exploring the area"
            ]
        elif risk_level == RiskLevel.MODERATE:
            recommendations = [
                "🔔 Stay aware of surroundings",
                "🚕 Use registered transportation",
                "📍 Share your location with family",
                "🌙 Avoid isolated areas at night"
            ]
        elif risk_level == RiskLevel.HIGH:
            recommendations = [
                "⚠️ Exercise increased caution",
                "👥 Travel in groups when possible",
                "🏨 Stay in well-reviewed accommodations",
                "🚫 Avoid displaying valuables",
                "📞 Register with your embassy"
            ]
        else:  # CRITICAL
            recommendations = [
                "🚨 Consider alternative destinations",
                "🛡️ Essential travel only",
                "📋 Register with local authorities",
                "🆘 Keep emergency contacts ready",
                "🚪 Have evacuation plan prepared"
            ]
        
        return recommendations
    
    def calculate_route_safety_score(
        self,
        route_segments: List[Dict],
        city_safety_data: Dict[int, float]
    ) -> Tuple[float, Dict]:
        """
        Calculate overall safety score for a route
        
        Args:
            route_segments: List of route segments with city_id
            city_safety_data: Dict mapping city_id to crime_index
        
        Returns:
            Tuple of (safety_score, breakdown)
        """
        if not route_segments:
            return 50.0, {"green": 0, "orange": 100, "red": 0}
        
        green_distance = 0.0
        orange_distance = 0.0
        red_distance = 0.0
        
        for segment in route_segments:
            city_id = segment.get("city_id")
            distance = segment.get("distance", 1.0)
            
            crime_index = city_safety_data.get(city_id, 50.0)
            zone = self.classify_safety_zone(crime_index)
            
            if zone == "green":
                green_distance += distance
            elif zone == "orange":
                orange_distance += distance
            else:
                red_distance += distance
        
        total_distance = green_distance + orange_distance + red_distance
        
        if total_distance == 0:
            return 50.0, {"green": 0, "orange": 100, "red": 0}
        
        # Calculate weighted safety score
        safety_score = (
            (green_distance * 100) +
            (orange_distance * 60) +
            (red_distance * 20)
        ) / total_distance
        
        breakdown = {
            "green": round(green_distance / total_distance * 100, 1),
            "orange": round(orange_distance / total_distance * 100, 1),
            "red": round(red_distance / total_distance * 100, 1)
        }
        
        return round(safety_score, 1), breakdown
    
    def cluster_cities_by_safety(
        self,
        cities_data: List[Dict]
    ) -> Dict[str, List[int]]:
        """
        Cluster cities into safety categories using K-means-like approach
        
        Args:
            cities_data: List of dicts with 'id' and 'crime_index'
        
        Returns:
            Dict mapping zone name to list of city IDs
        """
        clusters = {
            "green": [],
            "orange": [],
            "red": []
        }
        
        for city in cities_data:
            zone = self.classify_safety_zone(city["crime_index"])
            clusters[zone].append(city["id"])
        
        return clusters
    
    def analyze_crime_trend(
        self,
        historical_data: List[Tuple[int, float]]
    ) -> Dict:
        """
        Analyze crime trend over time
        
        Args:
            historical_data: List of (year, crime_index) tuples
        
        Returns:
            Dict with trend analysis
        """
        if len(historical_data) < 2:
            return {"trend": "insufficient_data", "change": 0}
        
        # Sort by year
        sorted_data = sorted(historical_data, key=lambda x: x[0])
        indices = [d[1] for d in sorted_data]
        
        # Simple linear trend
        if len(indices) >= 2:
            avg_change = (indices[-1] - indices[0]) / len(indices)
            
            if avg_change > 3:
                trend = "increasing"
            elif avg_change < -3:
                trend = "decreasing"
            else:
                trend = "stable"
            
            return {
                "trend": trend,
                "avg_yearly_change": round(avg_change, 2),
                "current_index": indices[-1],
                "five_year_change": round(indices[-1] - indices[0], 2) if len(indices) >= 5 else None
            }
        
        return {"trend": "stable", "change": 0}


# Singleton instance
safety_ml_service = SafetyMLService()
