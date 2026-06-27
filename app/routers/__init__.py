"""
Makkawi Smart - Routers Package
"""
from app.routers.auth import router as auth_router
from app.routers.pages import router as pages_router
from app.routers.dashboard import router as dashboard_router

__all__ = ["auth_router", "pages_router", "dashboard_router"]
