from typing import List

from pony import orm
from psycopg2.extras import DictCursor

from entities import RSS, RSSSource
from interfaces.rss_repository_interface import RSSRepositoryInterface
from models import RSS as RSSDB, RSSSource as RSSSourceDB
from exceptions import RepositoryException, error_status
from settings.connections import Postgres


class RSSRepository(RSSRepositoryInterface):
    """
    RSS table related functionality
    """
    @classmethod
    def create(cls, model: RSS) -> RSS:
        query = """
                INSERT INTO public.RSS (title, description, link, source_id, pub_date)
                VALUES (%s, %s, %s, %s, %s) RETURNING ID;
                """
        if not (model.source and model.source.id):
            raise RepositoryException("Source id must be provided", error_code=error_status.VALIDATION_ERROR)
        title = model.title
        description = model.description if model.description else ''
        link = model.link
        source_id = model.source.id
        pub_date = model.pub_date.strftime("%Y-%m-%d %H:%M:%S.%f") if model.pub_date else None
        params = (title, description, link, source_id, pub_date)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        Postgres.connection_putback(conn)
        if result:
            model.id = result.get("id")
        return model

    @classmethod
    def get_list(cls, rss_ids: List[int]):
        rss_ids_tuple = tuple(rss_ids)
        query = """
                   select id, title, link, description, source_id, pub_date from RSS
                   where id in %s
                """
        params = (rss_ids_tuple,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchall()
        Postgres.connection_putback(conn)
        if result:
            rss_list = [
                RSS(
                    id=item["id"],
                    title=item["title"],
                    link=item["link"],
                    description=item["description"],
                    source=RSSSource(id=item["source_id"]),
                    pub_date=item["pub_date"]
                )
                for item in
                result
            ]
            return rss_list
        return []
