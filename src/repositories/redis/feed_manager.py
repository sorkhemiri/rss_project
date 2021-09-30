from datetime import datetime

from settings.connections import RedisConnection


class FeedManager:
    PREFIX = "user:feed:"

    @classmethod
    def add_to_feed(cls, user_id: int, post_ids: list, date: datetime):
        user_feed_prefix = cls.PREFIX + "global:user:" + f"{user_id}"
        now_time = date.timestamp()
        data_values = []
        for post_id in post_ids:
            post_serial_id = f"{int(now_time)}{post_id}"
            data_values.append({post_id: post_serial_id})
        RedisConnection.add_values_to_set(key=user_feed_prefix, values=data_values)

    @classmethod
    def add_to_channel(cls, key: str, post_ids: list, date: datetime):
        user_feed_prefix = cls.PREFIX + "global:channel:" + key
        now_time = date.timestamp()
        data_values = []
        for post_id in post_ids:
            post_serial_id = f"{int(now_time)}{post_id}"
            data_values.append({post_id: post_serial_id})
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
        RedisConnection.get_set_values_range(
            key=user_feed_prefix, start=from_item, end=to_item)

    @classmethod
    def get_channel(cls, key: str, page: int = 1, limit: int = 10):
        user_feed_prefix = cls.PREFIX + "global:channel:" + key
        from_item = ((page - 1) * limit)
        to_item = (page * limit) - 1
        RedisConnection.get_set_values_range(
            key=user_feed_prefix, start=from_item, end=to_item)
