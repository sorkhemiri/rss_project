import abc
from typing import Optional
from uuid import UUID

from .repository import RepositoryInterface


class UserAuthRepositoryInterface(RepositoryInterface):
    """
    User Authentication related functionality
    """

    @classmethod
    @abc.abstractmethod
    def login(cls, uid: UUID) -> dict:
        pass

    @classmethod
    @abc.abstractmethod
    def logout(cls, uid: str) -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def authenticated(cls, access_token: str) -> Optional[UUID]:
        pass

    @classmethod
    @abc.abstractmethod
    def get_authentication_data(cls, uid: str) -> Optional[dict]:
        pass

    @classmethod
    @abc.abstractmethod
    def refresh_access(cls, refresh_token: str) -> Optional[dict]:
        pass
