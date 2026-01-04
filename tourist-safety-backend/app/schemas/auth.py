"""
Authentication Schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class GoogleAuthRequest(BaseModel):
    """Request for Google OAuth authentication"""
    token: str  # Google ID token from frontend


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"


class UserResponse(BaseModel):
    """User information response"""
    id: int
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """Create a new user"""
    email: EmailStr
    name: Optional[str] = None
    password: Optional[str] = None  # Optional for OAuth users
    google_id: Optional[str] = None


class UserUpdate(BaseModel):
    """Update user profile"""
    name: Optional[str] = None
    picture: Optional[str] = None
    saved_routes: Optional[str] = None
    favorite_cities: Optional[str] = None


# Mock user for development without Google setup
class MockLoginRequest(BaseModel):
    """Mock login for development"""
    email: EmailStr
    name: Optional[str] = "Test User"
