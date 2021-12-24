from typing import Optional

from interfaces.validator import ValidatorInterface


class RegisterValidator(ValidatorInterface):
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
