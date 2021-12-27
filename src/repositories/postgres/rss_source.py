from typing import List

from pony import orm
from psycopg2.extras import DictCursor

from entities import RSSSource
from exceptions import RepositoryException
from interfaces.rss_source_repository_interface import RSSSourceRepositoryInterface
from settings.connections import Postgres


class RSSSourceRepository(RSSSourceRepositoryInterface):
    """
    RSSSource table related functionality
    """

    @classmethod
    def create(cls, model: RSSSource):
        query = """
        INSERT INTO public.RSSSOURCE (key, title, description, link)
        VALUES (%s, %s, %s, %s);
        """
        key = model.key
        title = model.title
        description = model.description if model.description else ''
        link = model.link
        params = (key, title, description, link)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
        return model

    @classmethod
    def delete(cls, key: str):
        query = """
            DELETE FROM public.RSSSOURCE WHERE key=%s;
            """
        params = (key,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)

    @classmethod
    def get_list(cls, offset: int = 0, limit: int = 10) -> List[RSSSource]:
        query = """ select title, key, description, link
                    from public.RSSSource offset %s limit %s"""
        params = (offset, limit)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            rss_source_data = curs.fetchall()
            rss_source_entities = [
                RSSSource(
                          title=item["title"],
                          key=item["key"],
                          description=item["description"],
                          link=item["link"]
                          ) for item in rss_source_data
                                   ]
            return rss_source_entities

    @classmethod
    def check_source_key_exists(cls, key: str) -> bool:
        query = """
                   select id from RSSSource where
                   key = %s
                """
        params = (key,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        if result:
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

    @classmethod
    def get_sources_id_by_key(cls, source_key: str) -> int:
        query = """
                   select id from RSSSource where
                   key = %s
                """
        params = (source_key,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
            source_id = result.get("id")
        return source_id
