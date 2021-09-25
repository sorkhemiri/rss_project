from pony.orm import Required, Optional, Set

from .base import db


class RSSSource(db.Entity):
    name = Required(str, max_len=100)
    is_deleted = Optional(bool, sql_default=False)
    rss_content = Set('RSS', reverse='source')
    subscriptions = Set("Subscription", reverse='source')

    def __str__(self):
        return self.name
