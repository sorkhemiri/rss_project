from pony.orm import Required, Optional, Set

from .base import db


class User(db.Entity):
    first_name = Optional(str, max_len=100)
    last_name = Optional(str, max_len=100)
    username = Required(str, max_len=200, unique=True)
    password = Required(str, max_len=500)
    is_deleted = Optional(bool, sql_default=False)
    subscriptions = Set("Subscription", reverse="user")
    likes = Set("Like", reverse="user")

    def __str__(self):
        return self.username
