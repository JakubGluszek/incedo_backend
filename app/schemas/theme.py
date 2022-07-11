from typing import Optional
from pydantic import BaseModel


class ThemeBase(BaseModel):
    primary: str
    secondary: str
    accent: str
    neutral: str
    base: str
    info: str
    success: str
    warning: str
    error: str


class ThemeCreate(ThemeBase):
    name: str


class ThemeUpdate(BaseModel):
    name: Optional[str] = None
    primary: Optional[str] = None
    secondary: Optional[str] = None
    accent: Optional[str] = None
    neutral: Optional[str] = None
    base: Optional[str] = None
    info: Optional[str] = None
    success: Optional[str] = None
    warning: Optional[str] = None
    error: Optional[str] = None


class Theme(ThemeBase):
    id: int
    user_id: int
    name: str


class ThemeOut(ThemeBase):
    id: int
    name: str
