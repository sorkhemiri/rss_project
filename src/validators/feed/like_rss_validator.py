from interfaces.validator import ValidatorInterface

from entities import User


class LikeRSSValidator(ValidatorInterface):
    rss_id: int
    user: User
