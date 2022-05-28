from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_repeat: str


class UserUpdate(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    username: str
    avatar: HttpUrl
    email_verified: bool
    is_super: bool


class UserOut(BaseModel):
    id: int
    username: str
    avatar: HttpUrl
    email_verified: bool
    is_super: bool
