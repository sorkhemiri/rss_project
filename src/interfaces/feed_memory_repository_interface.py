import abc
from datetime import datetime

from .repository import RepositoryInterface


class FeedMemoryRepositoryInterface(RepositoryInterface):
    """
    This repository remembers feed for a while to
    avoid redundancy.
    """

    @classmethod
    @abc.abstractmethod
    def add_to_memory(cls, key: str, post_ids: list, date: datetime):
        pass

    @classmethod
    @abc.abstractmethod
    def get_memory(cls, key: str, date: datetime, days: int = 1):
        pass
