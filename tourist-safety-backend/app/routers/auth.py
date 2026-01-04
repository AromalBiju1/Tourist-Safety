"""
Authentication Router - Google OAuth and JWT endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.services.auth_service import auth_service
from app.schemas.auth import (
    GoogleAuthRequest, 
    TokenResponse, 
    UserResponse, 
    UserUpdate,
    MockLoginRequest
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current authenticated user from JWT token"""
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = auth_service.decode_token(token)
    
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    return user


async def require_auth(
    user: Optional[User] = Depends(get_current_user)
) -> User:
    """Require authentication - raises 401 if not authenticated"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/google", response_model=TokenResponse)
async def google_auth(
    request: GoogleAuthRequest,
    db: Session = Depends(get_db)
):
    """Authenticate with Google OAuth token"""
    # Verify Google token
    google_data = auth_service.verify_google_token(request.token)
    
    if not google_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )
    
    # Find or create user
    user = db.query(User).filter(User.google_id == google_data["google_id"]).first()
    
    if not user:
        # Check if email exists
        user = db.query(User).filter(User.email == google_data["email"]).first()
        if user:
            # Link Google account to existing user
            user.google_id = google_data["google_id"]
            user.picture = google_data.get("picture")
        else:
            # Create new user
            user = User(
                email=google_data["email"],
                name=google_data.get("name", ""),
                picture=google_data.get("picture", ""),
                google_id=google_data["google_id"],
                is_verified=google_data.get("email_verified", False)
            )
            db.add(user)
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    # Create JWT token
    token_data = auth_service.create_user_token(user.id, user.email)
    
    return TokenResponse(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        user=UserResponse.model_validate(user)
    )


@router.post("/mock-login", response_model=TokenResponse)
async def mock_login(
    request: MockLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Mock login for development/testing without Google OAuth setup.
    DO NOT use in production!
    """
    # Find or create user
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        user = User(
            email=request.email,
            name=request.name or "Test User",
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create JWT token
    token_data = auth_service.create_user_token(user.id, user.email)
    
    return TokenResponse(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(require_auth)):
    """Get current authenticated user"""
    return UserResponse.model_validate(user)


@router.put("/me", response_model=UserResponse)
async def update_me(
    update: UserUpdate,
    user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    if update.name is not None:
        user.name = update.name
    if update.picture is not None:
        user.picture = update.picture
    if update.saved_routes is not None:
        user.saved_routes = update.saved_routes
    if update.favorite_cities is not None:
        user.favorite_cities = update.favorite_cities
    
    db.commit()
    db.refresh(user)
    
    return UserResponse.model_validate(user)


@router.post("/logout")
async def logout(user: User = Depends(require_auth)):
    """Logout - client should discard the token"""
    # In a more complete system, you'd blacklist the token here
    return {"message": "Logged out successfully"}


@router.get("/check")
async def check_auth(user: Optional[User] = Depends(get_current_user)):
    """Check if user is authenticated"""
    if user:
        return {
            "authenticated": True,
            "user": UserResponse.model_validate(user)
        }
    return {"authenticated": False, "user": None}
