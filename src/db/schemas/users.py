from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr

from db.schemas.items import Item


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_staff: bool


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str = None
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    is_staff: bool = None


class User(UserBase):
    id: UUID
    picture: str = None
    is_active: bool
    is_superuser: bool
    last_login_at: datetime = None
    created_at: datetime
    updated_at: datetime = None

    items: list[Item] = []

    class Config:
        orm_mode = True
