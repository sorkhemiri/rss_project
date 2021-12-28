import abc
from typing import List

from entities import RSSSource
from .repository import RepositoryInterface


class RSSSourceRepositoryInterface(RepositoryInterface):
    """
    RSSSource table related functionality
    """

    @classmethod
    @abc.abstractmethod
    def create(cls, model: RSSSource) -> RSSSource:
        pass

    @classmethod
    @abc.abstractmethod
    def delete(cls, key: str) -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def get_list(cls, offset: int = 0, limit: int = 10) -> List[RSSSource]:
        pass

    @classmethod
    @abc.abstractmethod
    def check_source_key_exists(cls, key: str) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def get_sources_key(cls, source_id: int) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def get_sources_id_by_key(cls, source_key: str) -> int:
        pass
