import os

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pytest
from psycopg2.extras import DictCursor
from psycopg2.pool import SimpleConnectionPool
from tortoise import run_async

from generate_db import generate_schemas
from settings import env_config
from settings.connections import Postgres


@pytest.fixture(autouse=True, scope="session")
def database_session_fixture():
    connection = connect(
        user=env_config.postgres_user,
        password=env_config.postgres_password,
        host=env_config.postgres_host,
        port=env_config.postgres_port,
    )
    db_name = "test_application"
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    q1 = """
    drop database if exists test_application;
    """
    q2 = """
    CREATE DATABASE test_application;
    """

    with connection.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(q1)
        curs.execute(q2)
        curs.close()
    connection.close()
    original_pool = Postgres._pool
    original_db = env_config.postgres_db
    env_config.postgres_db = db_name
    run_async(generate_schemas())
    pool = SimpleConnectionPool(
        user=env_config.postgres_user,
        password=env_config.postgres_password,
        host=env_config.postgres_host,
        port=env_config.postgres_port,
        database=env_config.postgres_db,
        minconn=1,
        maxconn=env_config.postgres_max_connections,
    )
    Postgres._pool = pool
    print("DB TEST INIT")
    yield
    print("DB TEST END")
    pool.closeall()
    connection = connect(
        user=env_config.postgres_user,
        password=env_config.postgres_password,
        host=env_config.postgres_host,
        port=env_config.postgres_port,
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with connection.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(q1)
    env_config.postgres_db = original_db
    Postgres._pool = original_pool


# @pytest.fixture
# def postgres_patch(monkeypatch):
#     def connection():
#         return connect(
#                         user=env_config.postgres_user,
#                         password=env_config.postgres_password,
#                         host=env_config.postgres_host,
#                         port=env_config.postgres_port,
#                         database=env_config.postgres_db,
#                     )
#
#     def always_none():
#         return None
#
#     monkeypatch.setattr(Postgres, "get_connection", connection)
#     monkeypatch.setattr(Postgres, "connection_putback", always_none)
#
# database_session_fixture()
