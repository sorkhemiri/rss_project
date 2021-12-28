from pydantic import validator

from interfaces.validator import ValidatorInterface


class GetRSSSourceFeedValidator(ValidatorInterface):
    source_key: str
    page: int = 1
    limit: int = 10

    @validator("limit")
    def limit_normalizer(cls, v):
        if v > 100:
            v = 100
        return v
