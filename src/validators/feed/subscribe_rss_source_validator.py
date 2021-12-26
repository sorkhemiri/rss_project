from interfaces.validator import ValidatorInterface

from entities import User


class SubscribeRSSSourceValidator(ValidatorInterface):
    user: User
    source_id: int
