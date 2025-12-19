from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"

class UserSummary(BaseModel):
    user_id: str
    email: EmailStr
    username: str
    role: UserRole
    profile_img: str

class UserDetail(UserSummary):
    created_at: datetime
    last_login: datetime
    preferences: dict

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    profile_img: Optional[str] = None
    preferences: Optional[dict] = None
    role: Optional[UserRole] = None

class UserSignin(BaseModel):
    email: EmailStr
    password: str

class UserListResponse(BaseModel):
    items: list[UserSummary]
    total: int
