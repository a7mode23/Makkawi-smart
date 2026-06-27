"""
Makkawi Smart - Pages Router (Landing, Contact)
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Render the landing page."""
    return templates.TemplateResponse(request, "pages/landing.html")


@router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    """Render the contact page."""
    return templates.TemplateResponse(request, "pages/landing.html", context={"scroll_to": "contact"})
