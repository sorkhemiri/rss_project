from pony.orm import Required, Optional

from .base import db


class RSSSource(db.Entity):
    name = Required(str, max_len=100)
    is_deleted = Optional(sql_default=False)

    def __str__(self):
        return self.name
