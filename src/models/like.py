import datetime

from pony.orm import Required, Optional

from .base import db


class Like(db.Entity):
    rss = Optional("RSS", reverse="likes")
    user = Required("User", reverse="likes")
    is_deleted = Optional(sql_default=False)

    def __str__(self):
        return self.title
