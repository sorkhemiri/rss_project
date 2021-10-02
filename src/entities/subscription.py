from typing import Optional

from pydantic import BaseModel

from .user import User
from .rss_source import RSSSource


class Subscription(BaseModel):
    id: Optional[int] = None
    source: Optional[RSSSource] = None
    user: Optional[User] = None
