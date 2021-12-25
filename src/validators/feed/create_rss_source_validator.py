from typing import Optional

from interfaces.validator import ValidatorInterface


class CreateRSSSourceValidator(ValidatorInterface):
    key: str
    title: str
    description: Optional[str]
    link: str
