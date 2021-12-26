from typing import Optional

from interfaces.validator import ValidatorInterface


class RSSSourceListValidator(ValidatorInterface):
    limit: int = 10
    offset: int = 0
