from pydantic import BaseModel, Field
from typing import Optional


class Coordinates(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class RouteRequest(BaseModel):
    """Request for route calculation"""
    origin: Coordinates
    destination: Coordinates
    preferences: Optional[dict] = Field(default_factory=lambda: {
        "avoid_high_risk": True,
        "prefer_main_roads": True
    })


class ZoneBreakdown(BaseModel):
    """Breakdown of route by safety zones"""
    green_percentage: float
    orange_percentage: float
    red_percentage: float
    green_distance_km: float
    orange_distance_km: float
    red_distance_km: float


class RouteOption(BaseModel):
    """A single route option with safety analysis"""
    route_id: str
    safety_score: float = Field(..., ge=0, le=100)
    classification: str  # "safe", "moderate", "risky"
    distance_km: float
    duration_min: float
    geometry: dict  # GeoJSON LineString
    zone_breakdown: ZoneBreakdown
    zones_passed: list[dict]  # List of zones with entry/exit points
    recommendations: list[str]  # Safety tips for this route


class RouteResponse(BaseModel):
    """Response with multiple route options"""
    origin: Coordinates
    destination: Coordinates
    calculated_at: str
    routes: list[RouteOption]
    safest_route_id: str
    fastest_route_id: str


class RouteSafetyTip(BaseModel):
    """Safety tip for a specific route segment"""
    zone: str
    message: str
    icon: str  # warning, info, success
