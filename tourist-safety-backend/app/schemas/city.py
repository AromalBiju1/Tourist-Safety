from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class SafetyZoneEnum(str, Enum):
    GREEN = "green"
    ORANGE = "orange"
    RED = "red"


class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    population: Optional[int] = None


class CityCreate(CityBase):
    crime_index: Optional[float] = 50.0


class CityResponse(CityBase):
    id: int
    crime_index: float
    safety_zone: str
    
    class Config:
        from_attributes = True


class CityWithSafety(CityResponse):
    """Extended city response with safety details"""
    safety_color: str = Field(description="Hex color for the safety zone")
    safety_description: str = Field(description="Human-readable safety description")
    
    @staticmethod
    def get_safety_color(zone: str) -> str:
        colors = {
            "green": "#22c55e",
            "orange": "#f97316", 
            "red": "#ef4444"
        }
        return colors.get(zone, "#6b7280")
    
    @staticmethod
    def get_safety_description(zone: str) -> str:
        descriptions = {
            "green": "Safe - Low crime rate, recommended for tourists",
            "orange": "Moderate Risk - Exercise normal precautions",
            "red": "High Risk - Exercise increased caution"
        }
        return descriptions.get(zone, "Unknown")


class CitySafetyOverview(BaseModel):
    """Summary of cities by safety zone"""
    total_cities: int
    green_count: int
    orange_count: int
    red_count: int
    cities: list[CityWithSafety]
