from interfaces.validator import ValidatorInterface
from entities import User


class UserSubscriptionsListValidator(ValidatorInterface):
    user: User
    limit: int = 10
    offset: int = 0
