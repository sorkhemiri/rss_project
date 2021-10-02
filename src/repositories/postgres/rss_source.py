from typing import List

from pony import orm

from entities import RSSSource
from models import RSSSource as RSSSourceDB
from models import db
from utils.exceptions import RepositoryException


class RSSSourceRepository:

    @classmethod
    def create(cls, model: RSSSource):
        with orm.db_session:
            model_data = model.dict(exclude_defaults=True)
            source_db = RSSSourceDB(**model_data)
            orm.commit()
            model.id = source_db.id

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

    @classmethod
    def check_source_key_exists(cls, key: str) -> bool:
        with orm.db_session:
            if db.exists("select id from RSSSource where"
                         " key = $key and (is_deleted is null or is_deleted = FALSE)"):
                return True
            return False

    @classmethod
    def get_sources_key(cls, source_id: int) -> str:
        with orm.db_session:
            rss_source_keys = db.select("select key from RSSSource where"
                                       " id = $source_id "
                                       "and (is_deleted is null or is_deleted = FALSE) limit 1")
            if rss_source_keys:
                rss_source_key = rss_source_keys[0]
                return rss_source_key
            else:
                raise RepositoryException(message="source not found")
