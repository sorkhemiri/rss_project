from pydantic import BaseModel

from entities import User


class UnsubscribeRSSSourceValidator(BaseModel):
    user: User
    source_id: int
