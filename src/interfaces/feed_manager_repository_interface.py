import abc
from typing import List

from .repository import RepositoryInterface


class FeedManagerRepositoryInterface(RepositoryInterface):
    @classmethod
    @abc.abstractmethod
    def add_to_feed(cls, user_id: int, feed: List[tuple]):
        pass

    @classmethod
    @abc.abstractmethod
    def add_to_channel(cls, key: str, feed: List[tuple]):
        pass

    @classmethod
    @abc.abstractmethod
    def add_to_unseen(cls, user_id: int, post_ids: list):
        pass

    @classmethod
    @abc.abstractmethod
    def get_feed(cls, user_id: int, page: int = 1, limit: int = 10):
        pass

    @classmethod
    @abc.abstractmethod
    def get_channel(cls, key: str, page: int = 1, limit: int = 10):
        pass

    @classmethod
    @abc.abstractmethod
    def get_channel_all(cls, key: str):
        pass

    @classmethod
    @abc.abstractmethod
    def delete_from_feed(cls, user_id: int, values: List[str]):
        pass

    @classmethod
    @abc.abstractmethod
    def get_unseen(cls, user_id: int):
        pass

    @classmethod
    @abc.abstractmethod
    def remove_from_unseen(cls, user_id: int, post_ids: list):
        pass

    @classmethod
    @abc.abstractmethod
    def add_to_source_unseen(cls, user_id: int, source_key: str, post_ids: list):
        pass

    @classmethod
    @abc.abstractmethod
    def get_source_unseen(cls, user_id: int, source_key: str):
        pass

    @classmethod
    @abc.abstractmethod
    def remove_source_from_unseen(cls, user_id: int, source_key: str, post_ids: list):
        pass
