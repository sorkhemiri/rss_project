from datetime import datetime
from typing import List

from settings.connections import RedisConnection


class FeedManager:
    PREFIX = "user:feed:"

    @classmethod
    def add_to_feed(cls, user_id: int, feed: List[tuple]):
        user_feed_prefix = cls.PREFIX + "global:user:" + f"{user_id}"
        data_values = [{item[0]:item[1]} for item in feed]
        RedisConnection.add_values_to_set(key=user_feed_prefix, values=data_values)

    @classmethod
    def add_to_channel(cls, key: str, feed: List[tuple]):
        user_feed_prefix = cls.PREFIX + "global:channel:" + key
        data_values = [{item[0]:item[1]} for item in feed]
        RedisConnection.add_values_to_set(key=user_feed_prefix, values=data_values)

    @classmethod
    def add_to_unseen(cls, user_id: int, post_ids: list):
        user_unseen_prefix = cls.PREFIX + "user:" + f"{user_id}:" + "unseen"
        RedisConnection.push_values(key=user_unseen_prefix, values=post_ids)

    @classmethod
    def get_feed(cls, user_id: int, page: int = 1, limit: int = 10):
        user_feed_prefix = cls.PREFIX + "global:user:" + f"{user_id}"
        from_item = ((page - 1) * limit)
        to_item = (page * limit) - 1
        values = RedisConnection.get_set_values_range(
            key=user_feed_prefix, start=from_item, end=to_item)
        return values

    @classmethod
    def get_channel(cls, key: str, page: int = 1, limit: int = 10):
        user_feed_prefix = cls.PREFIX + "global:channel:" + key
        from_item = ((page - 1) * limit)
        to_item = (page * limit) - 1
        values = RedisConnection.get_set_values_range(
            key=user_feed_prefix, start=from_item, end=to_item)
        return values

    @classmethod
    def get_channel_all(cls, key: str):
        user_feed_prefix = cls.PREFIX + "global:channel:" + key
        values = RedisConnection.get_set_values_range(
            key=user_feed_prefix, start=0, end=-1)
        return values

    @classmethod
    def delete_from_feed(cls, user_id: int, values: List[str]):
        user_feed_prefix = cls.PREFIX + "global:user:" + f"{user_id}"
        values = RedisConnection.remove_values_from_set(
            key=user_feed_prefix, values=values)
        return values
