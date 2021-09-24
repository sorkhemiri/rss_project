from pony.orm import Required, Optional

from .base import db


class User(db.Entity):
    first_name = Optional(str, max_len=100)
    last_name = Optional(str, max_len=100)
    username = Required(str, max_len=200)
    password = Required(str, max_len=500)

    def __str__(self):
        return self.username
