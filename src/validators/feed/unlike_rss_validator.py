from pydantic import BaseModel

from entities import User


class UnlikeRSSValidator(BaseModel):
    rss_id: int
    user: User
