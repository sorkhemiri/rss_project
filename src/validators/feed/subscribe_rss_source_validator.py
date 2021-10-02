from pydantic import BaseModel

from entities import User


class SubscribeRSSSourceValidator(BaseModel):
    user: User
    source_id: int
