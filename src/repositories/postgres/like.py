from pony import orm
from psycopg2.extras import DictCursor

from entities import Like
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
        query = """select id from Like where rss_id=%s and user_id=%s"""
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
        query = """select id from Like
                   where rss = %(rss_id)d and user = %(user_id)d
                   and (is_deleted is null or is_deleted = FALSE)"""
        conn = Postgres.get_connection()
        with conn.cursor() as curs:
            curs.execute(query)
        Postgres.connection_putback(conn)
