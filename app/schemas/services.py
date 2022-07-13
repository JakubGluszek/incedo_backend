from typing import Optional
from pydantic import BaseModel


class NewRank(BaseModel):
    type: str
    id: int
    parent_id: Optional[int] = None
    rank: int
