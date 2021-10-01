from typing import Optional, List

from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from redis import BlockingConnectionPool, StrictRedis
from settings.config import env_config


class RedisConnection:
    _connection: Optional[StrictRedis] = None
    pool = BlockingConnectionPool(
        max_connections=5,
        timeout=200,
        host=env_config.redis_host,
        port=env_config.redis_port,
        password=env_config.redis_password,
        username=env_config.redis_user,
    )

    @classmethod
    def get_connection(cls):
        if not cls._connection:
            cls._connection = StrictRedis(connection_pool=cls.pool)
        return cls._connection

    @classmethod
    def get_value(cls, key):
        cls.get_connection()
        value = cls._connection.get(key)
        if value:
            value = value.decode("utf-8")
        return value

    @classmethod
    def exists_key(cls, key):
        cls.get_connection()
        return True if cls._connection.exists(key) == 1 else False

    @classmethod
    def set_value(cls, key, value, exp: Optional[int] = None):
        cls.get_connection()
        cls._connection.set(key, value)
        if exp:
            cls._connection.expire(key, time=exp)

    @classmethod
    def delete_key(cls, key):
        cls.get_connection()
        cls._connection.delete(key)

    @classmethod
    def get_keys_with_prefix(cls, prefix: str):
        cls.get_connection()
        return [item.decode("utf-8") for item in cls._connection.keys(prefix + "*")]

    @classmethod
    def push_values(cls, key, values: list, exp: Optional[int] = None):
        if values:
            cls.get_connection()
            cls._connection.lpush(key, *values)
            if exp:
                cls._connection.expire(key, time=exp)

    @classmethod
    def get_all_list_values(cls, key: str):
        cls.get_connection()
        values_list = cls._connection.lrange(key, 0, -1)
        values_list = [item.decode("utf-8") for item in values_list]
        return values_list

    @classmethod
    def add_values_to_set(cls, key: str, values: List[dict], exp: Optional[int] = None):
        cls.get_connection()
        for item in values:
            cls._connection.zadd(key, mapping=item)
        if exp:
            cls._connection.expire(key, time=exp)

    @classmethod
    def get_set_values_range(cls, key: str, start: int, end: int):
        cls.get_connection()
        values_list = cls._connection.zrange(key, start=start, end=end, withscores=True)
        normal_values_list = []
        for value in values_list:
            rss_id = value[0].decode("utf-8")
            score = int(value[1])
            value_set = (rss_id, score)
            normal_values_list.append(value_set)
        return normal_values_list

    @classmethod
    def remove_values_from_set(cls, key: str, values: List[str]):
        cls.get_connection()
        cls._connection.zrem(key, *values)

    @classmethod
    def remove_values_from_list(cls, key: str, values: List[str]):
        if values:
            cls.get_connection()
            cls._connection.lrem(key, *values)

# class Postgres:
#     _connection = None
#     pool = ThreadedConnectionPool(
#         minconn=1,
#         maxconn=5,
#         user=env_config.postgres_user,
#         password=env_config.postgres_password,
#         host=env_config.postgres_host,
#         port=env_config.postgres_port,
#         database=env_config.postgres_db,
#     )
#
#     @classmethod
#     def get_connection(cls):
#         if not cls._connection or cls._connection.closed:
#             connection = cls.pool.getconn()
#             connection.autocommit = False
#             cls._connection = connection
#         return cls._connection
#
#     @classmethod
#     def get_dict_cursor(cls):
#         cls.get_connection()
#         cur = cls._connection.cursor(cursor_factory=DictCursor)
#         # cur.execute("SET TIME ZONE 'Asia/Tehran';")
#         return cur
