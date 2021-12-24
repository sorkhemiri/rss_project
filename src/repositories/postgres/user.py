from uuid import uuid4, UUID

from psycopg2.extras import DictCursor
from pony import orm

from entities import User
from interfaces.user_repository_interface import UserRepositoryInterface
from models import User as db
from settings.connections import Postgres
from utils import make_password
from exceptions import RepositoryException


class UserRepository(UserRepositoryInterface):

    @classmethod
    def check_username_exist(cls, username: str) -> bool:
        query = """select id from public.User
                   where username = %s"""
        params = (username,)
        conn = Postgres.get_connection()
        with conn.cursor() as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        if result:
            return True
        return False

    @classmethod
    def create(cls, model: User) -> User:
        model.password = make_password(password=model.password)
        username = model.username
        password = model.password
        first_name = model.first_name if model.first_name else ''
        last_name = model.last_name if model.last_name else ''
        uid = uuid4()
        query = """
        INSERT INTO public.User (username, password, first_name, last_name, uid)
        VALUES (%s, %s, %s, %s, %s);
        """
        params = (username, password, first_name, last_name, str(uid))
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            model.password = None
            model.uid = uid
            return model

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        password_hash = make_password(password=password)
        query = """
        select password from public.User
        where username = %s limit 1
        """
        params = (username,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
            db_password = result.get("password")
            if not db_password:
                raise RepositoryException(message="user password not set")
            if password_hash == db_password:
                return True
        return False

    @classmethod
    def get_uid_by_username(cls, username: str) -> UUID:
        query = """select uid from public.User
                   where username = %s limit 1"""
        params = (username,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
            uid = result.get("uid")
            if not uid:
                raise RepositoryException(message="user not found")
            return UUID(uid)

    @classmethod
    def check_user_exist(cls, uid: UUID) -> bool:
        query = """select uid from public.User
                   where uid = %s
                   and (is_deleted is null or is_deleted = FALSE)"""
        params = (str(uid),)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
            db_uid = result.get("uid")
        if db_uid == str(uid):
            return True
        return False
