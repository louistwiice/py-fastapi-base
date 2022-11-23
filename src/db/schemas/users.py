from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, constr

from db.schemas.items import Item


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_staff: bool


class UserCreate(UserBase):
    password: constr(min_length=3)


class UserUpdate(BaseModel):
    username: str = None
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    is_staff: bool = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: constr(min_length=3)
    confirm_password: constr(min_length=3)


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
