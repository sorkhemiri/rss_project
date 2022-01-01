from typing import List, Optional

from psycopg2.extras import DictCursor

from entities import RSSSource
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
        description = model.description if model.description else ""
        link = model.link
        params = (key, title, description, link)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
        Postgres.connection_putback(conn)
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
        Postgres.connection_putback(conn)

    @classmethod
    def get_list(cls, offset: int = 0, limit: int = 10) -> List[RSSSource]:
        query = """ select title, key, description, link
                    from public.RSSSource offset %s limit %s"""
        params = (offset, limit)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            rss_source_data = curs.fetchall()
        Postgres.connection_putback(conn)
        if rss_source_data:
            rss_source_entities = [
                RSSSource(
                    title=item["title"],
                    key=item["key"],
                    description=item["description"],
                    link=item["link"],
                )
                for item in rss_source_data
            ]
            return rss_source_entities
        return []

    @classmethod
    def get_sources(cls, offset: int = 0, limit: int = 10) -> List[RSSSource]:
        query = """ select title, key, description, link, id
                        from public.RSSSource offset %s limit %s"""
        params = (offset, limit)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            rss_source_data = curs.fetchall()
        Postgres.connection_putback(conn)
        if rss_source_data:
            rss_source_entities = [
                RSSSource(
                    id=item["id"],
                    title=item["title"],
                    key=item["key"],
                    description=item["description"],
                    link=item["link"],
                )
                for item in rss_source_data
            ]
            return rss_source_entities
        return []

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
        Postgres.connection_putback(conn)
        if result:
            return True
        return False

    @classmethod
    def get_sources_id_by_key(cls, source_key: str) -> Optional[int]:
        query = """
                   select id from RSSSource where
                   key = %s
                """
        params = (source_key,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        Postgres.connection_putback(conn)
        if result:
            source_id = result.get("id")
            return source_id
        return None

    @classmethod
    def make_update_need(cls, source_key: str):
        query = """
                       update public.RSSSource set need_update = TRUE where
                       key = %s
                    """
        params = (source_key,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
        Postgres.connection_putback(conn)

    @classmethod
    def unmake_update_need(cls, source_key: str):
        query = """
                       update public.RSSSource set need_update = FALSE where
                       key = %s
                    """
        params = (source_key,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
        Postgres.connection_putback(conn)
