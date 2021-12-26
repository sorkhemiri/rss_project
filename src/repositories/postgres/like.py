from pony import orm

from entities import Like
from interfaces.like_repository_interface import LikeRepositoryInterface
from models import User as UserDB, RSS as RSSDB, Like as LikeDB
from exceptions import RepositoryException, error_status
from settings.connections import Postgres


class LikeRepository(LikeRepositoryInterface):
    @classmethod
    def user_like_exist(cls, model: Like) -> bool:
        if not model.user and not model.user.id:
            raise RepositoryException(message="user id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)
        if not model.rss and not model.rss.id:
            RepositoryException(message="rss id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)
        with orm.db_session:
            query = """select id from Like where rss_id=%(model.rss.id)d and user_id=%(model.user.id)d"""
            conn = Postgres.get_connection()
            with conn.cursor() as curs:
                curs.execute(query)
                result = curs.fetchone()
            if result:
                return True
            return False

    @classmethod
    def create(cls, model: Like) -> Like:
        pass

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
