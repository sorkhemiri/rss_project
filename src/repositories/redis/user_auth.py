from typing import Optional
from uuid import UUID

from interfaces.user_auth_repository_interface import UserAuthRepositoryInterface
from settings.connections import RedisConnection
from settings.constants import (
    ACCESS_TOKEN_EXPIRATION_INTERVAL,
    ACCESS_TOKEN_LENGTH,
    REFRESH_TOKEN_LENGTH,
    REFRESH_TOKEN_EXPIRATION_INTERVAL,
)
from utils import make_random_hex, calculate_expiration_interval


class UserAuthRepository(UserAuthRepositoryInterface):
    """
    User Authentication related functionality
    """

    PREFIX = "user:auth:"
    ACCESS_PREFIX = PREFIX + "access:"
    REFRESH_PREFIX = PREFIX + "refresh:"

    @classmethod
    def login(cls, uid: UUID) -> dict:
        uid = str(uid)
        cls.logout(uid)
        access_token_prefix = cls.ACCESS_PREFIX + "token:"
        access_user_prefix = cls.ACCESS_PREFIX + "user:"

        refresh_token_prefix = cls.REFRESH_PREFIX + "token:"
        refresh_user_prefix = cls.REFRESH_PREFIX + "user:"

        access_token = make_random_hex(ACCESS_TOKEN_LENGTH)
        refresh_token = make_random_hex(REFRESH_TOKEN_LENGTH)

        access_token_key = access_token_prefix + access_token
        access_user_key = access_user_prefix + uid

        refresh_token_key = refresh_token_prefix + refresh_token
        refresh_user_key = refresh_user_prefix + uid

        RedisConnection.set_value(
            access_token_key, uid, exp=ACCESS_TOKEN_EXPIRATION_INTERVAL
        )
        RedisConnection.set_value(
            refresh_token_key, uid, exp=REFRESH_TOKEN_EXPIRATION_INTERVAL
        )

        RedisConnection.set_value(
            access_user_key, access_token, exp=ACCESS_TOKEN_EXPIRATION_INTERVAL
        )
        RedisConnection.set_value(
            refresh_user_key, refresh_token, exp=REFRESH_TOKEN_EXPIRATION_INTERVAL
        )

        token_data = {
            "access": {
                "token": access_token,
                "expire": calculate_expiration_interval(
                    ACCESS_TOKEN_EXPIRATION_INTERVAL
                ),
            },
            "refresh": {
                "token": refresh_token,
                "expire": calculate_expiration_interval(
                    REFRESH_TOKEN_EXPIRATION_INTERVAL
                ),
            },
        }
        return token_data

    @classmethod
    def logout(cls, uid: str) -> None:
        access_user_prefix = cls.ACCESS_PREFIX + "user:"
        refresh_user_prefix = cls.REFRESH_PREFIX + "user:"

        access_token_prefix = cls.ACCESS_PREFIX + "token:"
        refresh_token_prefix = cls.REFRESH_PREFIX + "token:"

        access_user_key = access_user_prefix + uid
        refresh_user_key = refresh_user_prefix + uid

        access_token = RedisConnection.get_value(access_user_key)
        refresh_token = RedisConnection.get_value(refresh_user_key)
        RedisConnection.delete_key(access_user_key)
        RedisConnection.delete_key(refresh_user_key)

        if access_token:
            access_token_key = access_token_prefix + access_token
            RedisConnection.delete_key(access_token_key)

        if refresh_token:
            refresh_token_key = refresh_token_prefix + refresh_token
            RedisConnection.delete_key(refresh_token_key)

    @classmethod
    def authenticated(cls, access_token: str) -> Optional[UUID]:
        access_token_prefix = cls.ACCESS_PREFIX + "token:"
        access_token_key = access_token_prefix + access_token
        uid = RedisConnection.get_value(access_token_key)
        if uid:
            return UUID(uid)
        return None

    @classmethod
    def get_authentication_data(cls, uid: str) -> Optional[dict]:
        access_user_prefix = cls.ACCESS_PREFIX + "user:"
        refresh_user_prefix = cls.REFRESH_PREFIX + "user:"

        access_user_key = access_user_prefix + uid
        refresh_user_key = refresh_user_prefix + uid

        access_token = RedisConnection.get_value(key=access_user_key)
        refresh_token = RedisConnection.get_value(key=refresh_user_key)
        if not access_token:
            return None

        access_token_ttl = RedisConnection.get_expire_time(key=access_user_key)
        refresh_token_ttl = RedisConnection.get_expire_time(key=refresh_user_key)

        token_data = {
            "access": {
                "token": access_token,
                "expire": calculate_expiration_interval(access_token_ttl),
            },
            "refresh": {
                "token": refresh_token,
                "expire": calculate_expiration_interval(refresh_token_ttl),
            },
        }
        return token_data

    @classmethod
    def refresh_access(cls, refresh_token: str) -> Optional[dict]:
        refresh_token_prefix = cls.REFRESH_PREFIX + "token:"
        refresh_token_key = refresh_token_prefix + refresh_token
        uid = RedisConnection.get_value(refresh_token_key)
        if uid:
            return cls.login(uid)
        else:
            return None
