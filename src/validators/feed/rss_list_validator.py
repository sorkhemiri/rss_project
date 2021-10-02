from pydantic import BaseModel, validator

from entities import User


class RSSListValidator(BaseModel):
    user: User
    page: int = 1
    limit: int = 10

    @validator('limit')
    def limit_normalizer(cls, v):
        if v > 100:
            v = 100
        return v
