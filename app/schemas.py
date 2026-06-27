"""
Makkawi Smart - Pydantic Schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.user import UserRole


# ─── Auth Schemas ───────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=120)
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


# ─── Router Schemas ─────────────────────────────────────────────────────────────

class RouterCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    vpn_ip_address: str = Field(..., max_length=45)
    api_username: str = Field(..., max_length=50)
    api_password: str = Field(..., max_length=255)
    api_port: int = Field(default=8728, ge=1, le=65535)


class RouterResponse(BaseModel):
    id: int
    name: str
    vpn_ip_address: str
    api_port: int
    connection_status: str
    is_active: bool

    class Config:
        from_attributes = True
