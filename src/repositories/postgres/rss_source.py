from typing import List

from pony import orm

from entities import RSSSource
from models import db


class RSSSourceRepository:

    @classmethod
    def get_list(cls) -> List[RSSSource]:
        with orm.db_session:
            rss_source_data = db.select("select id, name from RSSSource where is_deleted = FALSE")
            rss_source_entities = [RSSSource(**item) for item in rss_source_data]
            return rss_source_entities
