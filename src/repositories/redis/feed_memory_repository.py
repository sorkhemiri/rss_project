from datetime import datetime, timedelta

from interfaces.feed_memory_repository_interface import FeedMemoryRepositoryInterface
from settings.connections import RedisConnection
from settings.constants import FEED_STORE_TIME_OUT


class FeedMemoryRepository(FeedMemoryRepositoryInterface):
    """
    This repository remembers feed for a while to
    avoid redundancy.
    """

    PREFIX = "memory:feed:"

    @classmethod
    def add_to_memory(cls, key: str, post_ids: list, date: datetime):
        user_feed_prefix = cls.PREFIX + f"{key}:{date.strftime('%Y-%m-%d')}"
        RedisConnection.push_values(key=user_feed_prefix, values=post_ids, exp=FEED_STORE_TIME_OUT)

    @classmethod
    def get_memory(cls, key: str, date: datetime, days: int = 1):
        keys = []
        user_feed_prefix = cls.PREFIX + f"{key}:{date.strftime('%Y-%m-%d')}"
        keys.append(user_feed_prefix)
        days_to_keys = days
        while days_to_keys:
            key_date = date - timedelta(days=days_to_keys)
            source_feed_prefix = cls.PREFIX + f"{key}:{key_date.strftime('%Y-%m-%d')}"
            keys.append(source_feed_prefix)
            days_to_keys -= 1
        all_values = []
        for key in keys:
            values = RedisConnection.get_all_list_values(key)
            all_values.extend(values)
        return all_values
