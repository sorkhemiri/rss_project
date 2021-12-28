from typing import List

from pony import orm
from psycopg2.extras import DictCursor

from entities import Like, RSS
from interfaces.like_repository_interface import LikeRepositoryInterface
from exceptions import RepositoryException, error_status
from settings.connections import Postgres


class LikeRepository(LikeRepositoryInterface):
    """
    Like table related functionality
    """
    @classmethod
    def user_like_exist(cls, model: Like) -> bool:
        if not model.user and not model.user.id:
            raise RepositoryException(message="user id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)
        if not model.rss and not model.rss.id:
            RepositoryException(message="rss id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)
        rss_id = model.rss.id
        user_id = model.user.id
        query = """select id from public.Like where rss_id=%s and user_id=%s"""
        params = (rss_id, user_id)
        conn = Postgres.get_connection()
        with conn.cursor() as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        Postgres.connection_putback(conn)
        if result:
            return True
        return False

    @classmethod
    def create(cls, model: Like) -> Like:
        query = """
                INSERT INTO public.LIKE (rss_id, user_id)
                VALUES (%s, %s);
                """
        rss_id = model.rss.id
        user_id = model.user.id
        params = (rss_id, user_id)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
        Postgres.connection_putback(conn)
        return model

    @classmethod
    def delete(cls, model: Like):
        if not model.user and not model.user.id:
            raise RepositoryException(message="user id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)
        if not model.rss and not model.rss.id:
            RepositoryException(message="rss id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)
        rss_id = model.rss.id
        user_id = model.user.id
        query = """
        DELETE FROM public.LIKE WHERE rss_id=%s and user_id=%s;
        """
        params = (rss_id, user_id)
        conn = Postgres.get_connection()
        with conn.cursor() as curs:
            curs.execute(query, params)
        Postgres.connection_putback(conn)

    @classmethod
    def get_user_likes_list(cls, user_id: int, offset: int = 0, limit: int = 10) -> List[Like]:
        query = """
                    select r.title as title, r.id as id
                    from public.RSS as r
                    left join public.Like as l on r.id = l.rss_id
                    where l.user_id = %s limit %s offset %s
                """
        params = (user_id, limit, offset)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchall()
        Postgres.connection_putback(conn)
        if result:
            likes = [
                Like(rss=RSS(title=item["title"], id=item["id"])) for item in result
            ]
            return likes
        return []

    @classmethod
    def get_user_source_likes_list(cls, user_id: int, source_id: int, offset: int = 0, limit: int = 10)-> List[Like]:
        query = """
                            select r.title as title, r.id as id
                            from public.RSS as r
                            left join public.Like as l on r.id = l.rss_id
                            where l.user_id = %s and r.source_id = %s limit %s offset %s
                        """
        params = (user_id, source_id, limit, offset)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchall()
        Postgres.connection_putback(conn)
        if result:
            likes = [
                Like(rss=RSS(title=item["title"], id=item["id"])) for item in result
            ]
            return likes
        return []
