from pydantic import BaseModel, Field
from typing import Optional


class CrimeStatisticBase(BaseModel):
    year: int = Field(..., ge=2000, le=2030)
    murder: int = Field(default=0, ge=0)
    robbery: int = Field(default=0, ge=0)
    burglary: int = Field(default=0, ge=0)
    theft: int = Field(default=0, ge=0)
    riots: int = Field(default=0, ge=0)
    kidnapping: int = Field(default=0, ge=0)
    crimes_against_women: int = Field(default=0, ge=0)
    cyber_crimes: int = Field(default=0, ge=0)
    total_ipc_crimes: int = Field(default=0, ge=0)


class CrimeStatisticCreate(CrimeStatisticBase):
    city_id: int
    source: str = "NCRB"


class CrimeStatisticResponse(CrimeStatisticBase):
    id: int
    city_id: int
    crime_rate: float
    source: str
    
    class Config:
        from_attributes = True


class CrimeTrend(BaseModel):
    """Crime trend over years for a city"""
    city_name: str
    city_id: int
    years: list[int]
    crime_indices: list[float]
    trend: str  # "increasing", "decreasing", "stable"
