import datetime

from pony.orm import Required, Optional

from .base import db


class Subscription(db.Entity):
    source = Optional("RSSSource", reverse="subscriptions")
    user = Optional("User", reverse="subscriptions")
    is_deleted = Optional(bool, sql_default=False)
