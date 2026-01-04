from pydantic import BaseModel, Field
from typing import Optional


class AttractionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    category: Optional[str] = None
    description: Optional[str] = None
    rating: float = Field(default=4.0, ge=0, le=5)
    image_url: Optional[str] = None


class AttractionCreate(AttractionBase):
    city_id: int
    address: Optional[str] = None
    opening_hours: Optional[str] = None
    entry_fee: Optional[str] = None


class AttractionResponse(AttractionBase):
    id: int
    city_id: int
    address: Optional[str]
    review_count: int
    opening_hours: Optional[str]
    entry_fee: Optional[str]
    best_time_to_visit: Optional[str]
    popularity_score: float
    
    class Config:
        from_attributes = True


class AttractionWithCity(AttractionResponse):
    """Attraction with city safety info"""
    city_name: str
    city_state: str
    city_safety_zone: str
    city_safety_color: str


class AttractionSearchResult(BaseModel):
    """Search results for attractions"""
    query: str
    total_results: int
    attractions: list[AttractionWithCity]
