from pydantic import BaseModel

from interfaces.validator import ValidatorInterface


class RefreshAccessValidator(ValidatorInterface):
    access_token: str
    refresh_token: str
