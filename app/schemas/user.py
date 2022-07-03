from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: Optional[str] = Field(None, max_length=24)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=24)


class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    avatar: HttpUrl
    is_super: bool
    settings: UserSettings

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    username: str
    email: EmailStr
    avatar: HttpUrl
    is_super: bool

    class Config:
        orm_mode = True


from .user_settings import UserSettings

User.update_forward_refs()
