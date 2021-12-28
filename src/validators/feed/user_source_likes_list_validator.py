from interfaces.validator import ValidatorInterface
from entities import User


class UserSourceLikesListValidator(ValidatorInterface):
    user: User
    offset: int = 0
    limit: int = 10
    source_key: str
