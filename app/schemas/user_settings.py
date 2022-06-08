from typing import Optional
from pydantic import BaseModel, validator


class UserSettingsUpdate(BaseModel):
    time_diff: Optional[int] = None

    @validator("time_diff")
    def validate_diff(cls, v) -> int:
        if v < -11:
            raise ValueError("Time diff is too small")
        elif v > 12:
            raise ValueError("Time diff is too big")
        return v


class UserSettings(BaseModel):
    id: int
    time_diff: Optional[int]
    user_id: int

    class Config:
        orm_mode = True


class UserSettingsOut(BaseModel):
    time_diff: Optional[int]

    class Config:
        orm_mode = True
