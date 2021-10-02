from settings.connections import RedisConnection


class UserAuthenticate:
    PREFIX = "user:auth:"

    @classmethod
    def login(cls, user_id: int, token: str):
        token_with_prefix = cls.PREFIX + "token:" + token
        user_id_with_prefix = cls.PREFIX + "user_id:" + str(user_id)
        RedisConnection.set_value(token_with_prefix, user_id, exp=15770000)
        old_token = RedisConnection.get_value(user_id_with_prefix)
        if old_token:
            old_token_with_prefix = cls.PREFIX + "token:" + old_token
            RedisConnection.delete_key(old_token_with_prefix)
        RedisConnection.set_value(user_id_with_prefix, token, exp=15770000)

    @classmethod
    def logout(cls, token: str):
        token_with_prefix = cls.PREFIX + "token:" + token
        user_id = RedisConnection.get_value(token_with_prefix)
        if user_id:
            user_id_with_prefix = cls.PREFIX + "user_id:" + str(user_id)
            RedisConnection.delete_key(token_with_prefix)
            RedisConnection.delete_key(user_id_with_prefix)

    @classmethod
    def is_authenticated(cls, token: str):
        token_with_prefix = cls.PREFIX + "token:" + token
        user_id = RedisConnection.get_value(token_with_prefix)
        return user_id
