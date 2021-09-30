from typing import List

from pony import orm

from entities import RSSSource
from models import RSSSource as RSSSourceDB
from models import db


class RSSSourceRepository:

    @classmethod
    def create_rss_sources(cls):
        rss_source_data = [
            {
                "title": "ورزش سه | آخرین اخبار",
                "link": "http://varzesh3.com/rss/all",
                "key": "varzesh3",
                "description": "آخرين اخبار ورزشی",
            }
        ]
        with orm.db_session:
            for item in rss_source_data:
                source_db = RSSSourceDB(**item)
                orm.commit()

    @classmethod
    def get_list(cls) -> List[RSSSource]:
        with orm.db_session:
            rss_source_data = db.select(
                "select id, title, description"
                " from RSSSource where (is_deleted is null or is_deleted = FALSE)")
            rss_source_entities = [
                RSSSource(id=item[0],
                          title=item[1],
                          description=item[2]
                          ) for item in rss_source_data
                                   ]
            return rss_source_entities

    @classmethod
    def get_sources(cls) -> List[RSSSource]:
        with orm.db_session:
            rss_source_data = db.select(
                "select id, title, description, link, key"
                " from RSSSource where (is_deleted is null or is_deleted = FALSE)")
            rss_source_entities = [
                RSSSource(id=item[0],
                          title=item[1],
                          description=item[2],
                          link=item[3],
                          key=item[4],
                          ) for item in rss_source_data
            ]
            return rss_source_entities

    @classmethod
    def check_source_exists(cls, source_id: int) -> bool:
        with orm.db_session:
            if db.exists("select id from RSSSource where"
                         " id = $source_id and (is_deleted is null or is_deleted = FALSE)"):
                return True
            return False
