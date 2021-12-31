import pytest


@pytest.fixture(autouse=True, scope="session")
def database_session_fixture():
    print("Before Session")
    yield
    print("after session")
    conn.execute("drop database if exists app_automated_tests")
