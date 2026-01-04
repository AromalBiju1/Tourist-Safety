from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.routers import safety_router, attractions_router, routes_router, emergency_router, analytics_router, viz_router, auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("🚀 Starting Tourist Safety API...")
    init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## Tourist Safety & Assistance API
    
    A comprehensive API for tourist safety in India, providing:
    
    - 🗺️ **Safety Zones**: City-wise safety classification (Green/Orange/Red)
    - 🛤️ **Safe Routes**: Route calculation with safety scoring
    - 🏛️ **Attractions**: Tourist hotspot recommendations
    - 🆘 **Emergency**: Quick access to emergency contacts
    - 📊 **Analytics**: ML-powered safety predictions
    - 🔐 **Authentication**: Google OAuth + JWT
    
    ### Safety Zone Classification
    - 🟢 **Green**: Safe - Low crime rate
    - 🟠 **Orange**: Moderate Risk - Exercise normal precautions
    - 🔴 **Red**: High Risk - Exercise increased caution
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)  # Auth first
app.include_router(safety_router, prefix=settings.API_V1_PREFIX)
app.include_router(attractions_router, prefix=settings.API_V1_PREFIX)
app.include_router(routes_router, prefix=settings.API_V1_PREFIX)
app.include_router(emergency_router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics_router, prefix=settings.API_V1_PREFIX)
app.include_router(viz_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "auth": f"{settings.API_V1_PREFIX}/auth",
            "safety": f"{settings.API_V1_PREFIX}/safety",
            "attractions": f"{settings.API_V1_PREFIX}/attractions",
            "routes": f"{settings.API_V1_PREFIX}/routes",
            "emergency": f"{settings.API_V1_PREFIX}/emergency",
            "analytics": f"{settings.API_V1_PREFIX}/analytics",
            "viz": f"{settings.API_V1_PREFIX}/viz"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
