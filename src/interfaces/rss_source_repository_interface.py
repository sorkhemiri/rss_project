import abc
from typing import List

from entities import RSSSource
from .repository import RepositoryInterface


class RSSSourceRepositoryInterface(RepositoryInterface):
    @classmethod
    @abc.abstractmethod
    def create(cls, model: RSSSource) -> RSSSource:
        pass

    @classmethod
    @abc.abstractmethod
    def get_list(cls) -> List[RSSSource]:
        pass

    @classmethod
    @abc.abstractmethod
    def get_sources(cls) -> List[RSSSource]:
        pass

    @classmethod
    @abc.abstractmethod
    def check_source_exists(cls, key: str) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def check_source_key_exists(cls, key: str) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def get_sources_key(cls, source_id: int) -> str:
        pass
