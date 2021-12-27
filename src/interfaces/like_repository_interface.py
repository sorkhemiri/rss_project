import abc
from typing import List

from entities import Like
from .repository import RepositoryInterface


class LikeRepositoryInterface(RepositoryInterface):
    """
    Like table related functionality
    """

    @classmethod
    @abc.abstractmethod
    def user_like_exist(cls, model: Like) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def create(cls, model: Like) -> Like:
        pass

    @classmethod
    @abc.abstractmethod
    def delete(cls, model: Like):
        pass

    @classmethod
    @abc.abstractmethod
    def get_user_likes_list(cls, user_id: int, offset: int = 0, limit: int = 10) -> List[Like]:
        pass
