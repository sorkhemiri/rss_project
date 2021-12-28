from pydantic import validator

from interfaces.validator import ValidatorInterface


class RSSSourceListValidator(ValidatorInterface):
    limit: int = 10
    offset: int = 0

    @validator("limit")
    def limit_normalizer(cls, v):
        if v > 100:
            v = 100
        return v
