from pony.orm import Required, Optional, Set

from .base import db


class RSSSource(db.Entity):
    title = Required(str, max_len=100)
    link = Required(str, max_len=800)
    description = Required(str, max_len=800)
    is_deleted = Optional(bool, sql_default=False)
    rss_content = Set('RSS', reverse='source')
    subscriptions = Set("Subscription", reverse='source')

    def __str__(self):
        return self.title
