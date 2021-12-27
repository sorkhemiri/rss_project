import abc
from typing import List

from entities import RSS
from .repository import RepositoryInterface


class RSSRepositoryInterface(RepositoryInterface):
    """
    RSS table related functionality
    """

    @classmethod
    @abc.abstractmethod
    def create(cls, model: RSS) -> RSS:
        pass

    @classmethod
    @abc.abstractmethod
    def get_list(cls, rss_ids: List[int]):
        pass
