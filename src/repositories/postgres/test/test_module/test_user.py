from uuid import uuid4, UUID

from psycopg2.extras import DictCursor

from entities import User
from repositories.postgres import UserRepository
from settings.connections import Postgres


class UserRepositoryTestCase:
    @staticmethod
    def test_input():
        user = User()
        user.username = "test1"
        user.first_name = "mahdi"
        user.last_name = "miri"
        user.password = "test_0123456789"
        UserRepository.create(model=user)
        connection = Postgres.get_connection()
        query = """
        select id, username, first_name, last_name, uid
        from public.User where username = %s limit 1 
        """
        with connection.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, (user.username,))
            result = curs.fetchone()
        Postgres.connection_putback(connection)
        assert user.username == result.get("username")
        assert user.first_name == result.get("first_name")
        assert user.last_name == result.get("last_name")
        assert result.get("uid")
        assert result.get("id")
