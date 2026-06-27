"""
Makkawi Smart - Main Application Entry Point
B2B SaaS Platform for MikroTik Router Management
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.config import get_settings
from app.database import init_db
from app.routers.auth import router as auth_router
from app.routers.pages import router as pages_router
from app.routers.dashboard import router as dashboard_router

settings = get_settings()


# ─── Application Lifespan ───────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    print("⚡ Makkawi Smart - Starting up...")
    await init_db()
    print("✓ Database initialized")
    print(f"✓ Running in {'DEBUG' if settings.DEBUG else 'PRODUCTION'} mode")
    yield
    print("⚡ Makkawi Smart - Shutting down...")


# ─── FastAPI App ────────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="B2B SaaS Platform for MikroTik Router Management via VPN",
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(dashboard_router)


# ─── Exception Handlers ─────────────────────────────────────────────────────────

@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc):
    """Redirect unauthorized users to login page."""
    return RedirectResponse(url="/auth/login", status_code=303)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors."""
    return RedirectResponse(url="/", status_code=303)


# ─── Run with Uvicorn ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
