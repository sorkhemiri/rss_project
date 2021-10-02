from datetime import datetime, timedelta

from settings.connections import RedisConnection


class FeedMemory:
    PREFIX = "memory:feed:"

    @classmethod
    def add_to_memory(cls, key: str, post_ids: list, date: datetime):
        user_feed_prefix = cls.PREFIX + f"{key}:{date.strftime('%Y-%m-%d')}"
        RedisConnection.push_values(key=user_feed_prefix, values=post_ids, exp=86400)

    @classmethod
    def get_memory(cls, key: str, date: datetime, days: int = 1):
        keys = []
        user_feed_prefix = cls.PREFIX + f"{key}:{date.strftime('%Y-%m-%d')}"
        keys.append(user_feed_prefix)
        days_to_keys = days
        while days_to_keys:
            key_date = date - timedelta(days=days_to_keys)
            user_feed_prefix = cls.PREFIX + f"{key}:{key_date.strftime('%Y-%m-%d')}"
            keys.append(user_feed_prefix)
            days_to_keys -= 1
        all_values = []
        for key in keys:
            values = RedisConnection.get_all_list_values(key)
            all_values.extend(values)
        return all_values

    # @classmethod
    # def get_feed(cls, user_id: int, page: int = 1, limit: int = 10):
    #     user_feed_prefix = cls.PREFIX + "global:user:" + f"{user_id}"
    #     from_item = ((page - 1) * limit)
    #     to_item = (page * limit) - 1
    #     RedisConnection.get_set_values_range(
    #         key=user_feed_prefix, start=from_item, end=to_item)
