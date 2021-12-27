from interfaces.validator import ValidatorInterface
from entities import User


class UnsubscribeRSSSourceValidator(ValidatorInterface):
    user: User
    source_key: str
