from typing import Optional
from uuid import uuid4, UUID

from psycopg2.extras import DictCursor

from entities import User
from interfaces.user_repository_interface import UserRepositoryInterface
from settings.connections import Postgres
from utils import make_password
from exceptions import RepositoryException


class UserRepository(UserRepositoryInterface):
    """
    User table related functionality
    """

    @classmethod
    def check_username_exist(cls, username: str) -> bool:
        query = """select id from public.User
                   where username = %s"""
        params = (username,)
        conn = Postgres.get_connection()
        with conn.cursor() as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        Postgres.connection_putback(conn)
        if result:
            return True
        return False

    @classmethod
    def create(cls, model: User) -> User:
        model.password = make_password(password=model.password)
        username = model.username
        password = model.password
        first_name = model.first_name if model.first_name else ""
        last_name = model.last_name if model.last_name else ""
        uid = uuid4()
        query = """
        INSERT INTO public.User (username, password, first_name, last_name, uid)
        VALUES (%s, %s, %s, %s, %s);
        """
        params = (username, password, first_name, last_name, str(uid))
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
        Postgres.connection_putback(conn)
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
        Postgres.connection_putback(conn)
        if result:
            db_password = result.get("password")
            if not db_password:
                raise RepositoryException(message="user password not set")
            if password_hash == db_password:
                return True
        return False

    @classmethod
    def get_uid_by_username(cls, username: str) -> Optional[UUID]:
        query = """select uid from public.User
                   where username = %s limit 1"""
        params = (username,)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        Postgres.connection_putback(conn)
        if result:
            uid = result.get("uid")
            if not uid:
                raise RepositoryException(message="user not found")
            return UUID(uid)
        return None

    @classmethod
    def check_user_exist(cls, uid: UUID) -> bool:
        query = """
                   select uid from public.User
                   where uid = %s
                """
        params = (str(uid),)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        Postgres.connection_putback(conn)
        if result:
            db_uid = result.get("uid")
            if db_uid == str(uid):
                return True
        return False

    @classmethod
    def get_user_id_by_uid(cls, uid: UUID) -> Optional[int]:
        query = """select id from public.User
                   where uid = %s"""
        params = (str(uid),)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        Postgres.connection_putback(conn)
        if result:
            db_id = result.get("id")
            return db_id
        return None

    @classmethod
    def is_admin(cls, uid: UUID) -> bool:
        query = """select id from public.User
                       where uid = %s and is_admin = TRUE"""
        params = (str(uid),)
        conn = Postgres.get_connection()
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, params)
            result = curs.fetchone()
        Postgres.connection_putback(conn)
        if result:
            db_id = result.get("id")
            if db_id:
                return True
        return False
