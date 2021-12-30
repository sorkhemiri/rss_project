from pydantic import validator

from entities import User
from interfaces.validator import ValidatorInterface


class UserFeedValidator(ValidatorInterface):
    user: User
    page: int = 1
    limit: int = 10

    @validator("limit")
    def limit_normalizer(cls, v):
        if v > 100:
            v = 100
        return v
