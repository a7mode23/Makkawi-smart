"""
Makkawi Smart - Dashboard Router
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request, current_user: User = Depends(get_current_user)):
    """Render the admin/user dashboard."""
    return templates.TemplateResponse(
        request, "dashboard/index.html",
        context={"user": current_user},
    )
