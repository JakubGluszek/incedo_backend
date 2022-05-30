from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class UserCreate(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    avatar: HttpUrl
    is_super: bool

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str
    avatar: HttpUrl

    class Config:
        orm_mode = True
