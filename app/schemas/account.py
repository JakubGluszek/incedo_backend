from typing import Optional

from pydantic import BaseModel


class Tokens(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
