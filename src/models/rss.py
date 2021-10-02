from datetime import datetime

from pony.orm import Required, Optional, Set

from .base import db


class RSS(db.Entity):
    title = Optional(str, max_len=300)
    link = Optional(str, max_len=500)
    description = Required(str, max_len=500)
    source = Optional("RSSSource", reverse="rss_content")
    pub_date = Optional(datetime)
    is_deleted = Optional(datetime, sql_default=False)
    likes = Set("Like", reverse="rss")

    def __str__(self):
        return self.title
