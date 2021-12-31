from typing import Optional

from pydantic import validator

from exceptions import ValidatorException, error_status
from interfaces.validator import ValidatorInterface


class CreateRSSSourceValidator(ValidatorInterface):
    key: str
    title: str
    description: Optional[str]
    link: str

    @validator("title")
    def empty_title(cls, v):
        if v == "":
            raise ValidatorException(
                message="title must not be empty",
                error_code=error_status.VALIDATION_ERROR,
            )
        return v

    @validator("link")
    def empty_link(cls, v):
        if v == "":
            raise ValidatorException(
                message="link must not be empty",
                error_code=error_status.VALIDATION_ERROR,
            )
        return v
