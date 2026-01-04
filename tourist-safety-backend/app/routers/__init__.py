from app.routers.safety import router as safety_router
from app.routers.attractions import router as attractions_router
from app.routers.routes import router as routes_router
from app.routers.emergency import router as emergency_router
from app.routers.analytics import router as analytics_router
from app.routers.visualization import router as viz_router
from app.routers.auth import router as auth_router

__all__ = [
    "safety_router",
    "attractions_router", 
    "routes_router",
    "emergency_router",
    "analytics_router",
    "viz_router",
    "auth_router"
]

