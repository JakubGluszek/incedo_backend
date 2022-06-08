from typing import Optional, ForwardRef
from pydantic import BaseModel, EmailStr, HttpUrl


UserSettings = ForwardRef("UserSettings")


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
    settings: UserSettings

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str
    avatar: HttpUrl

    class Config:
        orm_mode = True


User.update_forward_refs()
