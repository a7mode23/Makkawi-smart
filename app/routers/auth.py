"""
Makkawi Smart - Authentication Router (Login, Register)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User, UserRole
from app.auth import hash_password, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
templates = Jinja2Templates(directory="app/templates")


# ─── Registration Page ──────────────────────────────────────────────────────────

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Render the registration page."""
    return templates.TemplateResponse(request, "auth/register.html")


@router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """Handle user registration."""
    # Check if username already exists
    result = await db.execute(select(User).where(User.username == username))
    if result.scalar_one_or_none():
        return templates.TemplateResponse(
            request, "auth/register.html",
            context={"error": "Username already taken"},
            status_code=400,
        )

    # Check if email already exists
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none():
        return templates.TemplateResponse(
            request, "auth/register.html",
            context={"error": "Email already registered"},
            status_code=400,
        )

    # Create new user
    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hash_password(password),
        role=UserRole.CUSTOMER,
    )
    db.add(new_user)
    await db.commit()

    # Redirect to login with success message
    return RedirectResponse(url="/auth/login?registered=1", status_code=303)


# ─── Login Page ─────────────────────────────────────────────────────────────────

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, registered: int = 0):
    """Render the login page."""
    context = {}
    if registered:
        context["success"] = "Registration successful! Please log in."
    return templates.TemplateResponse(request, "auth/login.html", context=context)


@router.post("/login")
async def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """Handle user login."""
    user = await authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse(
            request, "auth/login.html",
            context={"error": "Invalid username or password"},
            status_code=401,
        )

    if not user.is_active:
        return templates.TemplateResponse(
            request, "auth/login.html",
            context={"error": "Account is deactivated"},
            status_code=403,
        )

    # Create JWT token
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value}
    )

    # Set token in HTTP-only cookie and redirect to dashboard
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=3600,
        samesite="lax",
    )
    return response


# ─── Logout ─────────────────────────────────────────────────────────────────────

@router.get("/logout")
async def logout_user():
    """Log out the user by clearing the auth cookie."""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response
