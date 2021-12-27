from interfaces.validator import ValidatorInterface

from entities import User


class UnlikeRSSValidator(ValidatorInterface):
    rss_id: int
    user: User
