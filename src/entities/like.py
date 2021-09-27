from typing import Optional

from pydantic import BaseModel

from .user import User
from .rss import RSS


class Like(BaseModel):
    id: Optional[int] = None
    rss: Optional[RSS] = None
    user: Optional[User] = None
