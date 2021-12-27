from typing import List

from pony import orm
from pony.orm import raw_sql
from psycopg2.extras import DictCursor

from entities import Subscription, User
from interfaces.subscription_repository_interface import SubscriptionRepositoryInterface
from models import Subscription as SubscriptionDB, RSSSource as RSSSourceDB, User as UserDB
from exceptions import RepositoryException, error_status
from settings.connections import Postgres


class SubscriptionRepository(SubscriptionRepositoryInterface):
    """
    Subscription table related functionality
    """
    @classmethod
    def create(cls, model: Subscription) -> Subscription:
        if not (model.source and model.source.id):
            raise RepositoryException(message="Source id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)
        if not(model.user and model.user.id):
            raise RepositoryException(message="user id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)

        query = """
                INSERT INTO public.RSSSOURCE (user_id, source_id)
                VALUES (%s, %s);
                """
        user_id = model.user.id
        source_id = model.source.id
        params = (user_id, source_id)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
        Postgres.connection_putback(conn)
        return model

    @classmethod
    def delete(cls, model: Subscription):
        if not model.user or not model.user.id:
            raise RepositoryException(message="user id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
        if not model.source or not model.source.id:
            raise RepositoryException(message="source id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
        source_id = model.source.id
        user_id = model.user.id
        query = """
        DELETE FROM public.RSSSOURCE WHERE source_id=%s and user_id=%s;
        """
        params = (user_id, source_id)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
        Postgres.connection_putback(conn)

    @classmethod
    def get_channel_subscriber_by_key(cls, key) -> List[Subscription]:
        with orm.db_session:
            sub_data = db.select(
                "select user"
                " from Subscription as s"
                " left join RSSSource as rs on rs.id = s.source"
                " where rs.key = $key and (s.is_deleted is null or s.is_deleted = FALSE)")
            sub_entities = [
                Subscription(user=User(id=item)) for item in sub_data
            ]
            return sub_entities

    @classmethod
    def check_subscription_exist(cls, model: Subscription) -> bool:
        if not model.user or not model.user.id:
            raise RepositoryException(message="user id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)
        if not model.source or not model.source.id:
            raise RepositoryException(message="source id must be provided", error_code=error_status.DOES_NOT_EXIST_ERROR)
        query = """select id from public.Subscription
                   where source_id=%s and user_id=%s"""
        params = (model.source.id, model.user.id)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            rss_source = curs.fetchone()
        Postgres.connection_putback(conn)
        if rss_source:
            return True
        return False
