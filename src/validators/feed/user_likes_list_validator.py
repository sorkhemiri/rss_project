from interfaces.validator import ValidatorInterface
from entities import User


class UserLikesListValidator(ValidatorInterface):
    user: User
    offset: int = 0
    limit: int = 10
