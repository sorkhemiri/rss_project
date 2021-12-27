import abc
from uuid import UUID

from entities import User
from .repository import RepositoryInterface


class UserRepositoryInterface(RepositoryInterface):
    """
    User table related functionality
    """

    @classmethod
    @abc.abstractmethod
    def check_username_exist(cls, username: str) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def create(cls, model: User) -> User:
        pass

    @classmethod
    @abc.abstractmethod
    def check_password(cls, username: str, password: str) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def get_uid_by_username(cls, username: str) -> int:
        pass

    @classmethod
    @abc.abstractmethod
    def check_user_exist(cls, uid: UUID) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def get_user_id_by_uid(cls, uid: UUID) -> int:
        pass
