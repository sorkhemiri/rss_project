import datetime

from pony.orm import Required, Optional

from .base import db


class RSS(db.Entity):
    title = Optional(str, max_len=300)
    link = Optional(str, max_len=500)
    description = Required(str, max_len=500)
    source = Optional("RSSSource", reverse="rss_content")
    pub_date = Required(datetime, max_len=500)
    is_deleted = Optional(sql_default=False)

    def __str__(self):
        return self.title
