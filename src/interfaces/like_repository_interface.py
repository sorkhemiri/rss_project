import abc

from entities import Like
from .repository import RepositoryInterface


class LikeRepositoryInterface(RepositoryInterface):

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
