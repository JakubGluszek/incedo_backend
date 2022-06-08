from typing import Optional, ForwardRef
from pydantic import BaseModel


User = ForwardRef("User")


class UserSettingsUpdate(BaseModel):
    time_diff: Optional[int] = None


class UserSettings(BaseModel):
    id: int
    time_diff: Optional[int]
    user_id: int
    user: User


class UserSettingsOut(BaseModel):
    time_diff: Optional[int]


UserSettings.update_forward_refs()
