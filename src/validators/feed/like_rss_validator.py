from pydantic import BaseModel

from entities import User


class LikeRSSValidator(BaseModel):
    rss_id: int
    user: User
