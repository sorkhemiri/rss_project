import re
from uuid import UUID

import pytest

from entities import User
from repositories.postgres import UserRepository
from repositories.redis import UserAuthRepository


@pytest.fixture
def username_present_patch(monkeypatch):
    def always_true(username):
        return True

    monkeypatch.setattr(UserRepository, "check_username_exist", always_true)


@pytest.fixture
def username_absent_patch(monkeypatch):
    def always_false(username):
        return False

    monkeypatch.setattr(UserRepository, "check_username_exist", always_false)


@pytest.fixture
def pattern_match_patch(monkeypatch):
    def always_match_patch(pattern, string):
        return True

    monkeypatch.setattr(re, "fullmatch", always_match_patch)


@pytest.fixture
def pattern_not_match_patch(monkeypatch):
    def always_not_match_patch(pattern, string):
        return False

    monkeypatch.setattr(re, "fullmatch", always_not_match_patch)


@pytest.fixture
def create_user_patch(monkeypatch):
    def user_patch(model: User):
        model.uid = UUID("bd9213db-8d4c-4da4-9c77-e8e92172fa88")
        model.password = None
        return model

    monkeypatch.setattr(UserRepository, "create", user_patch)


@pytest.fixture
def password_incorrect_patch(monkeypatch):
    def always_false(username, password):
        return False

    monkeypatch.setattr(UserRepository, "check_password", always_false)


@pytest.fixture
def password_correct_patch(monkeypatch):
    def always_true(username, password):
        return True

    monkeypatch.setattr(UserRepository, "check_password", always_true)


@pytest.fixture
def uid_by_username_patch(monkeypatch):
    def uid_provider(username):
        return UUID("bd9213db-8d4c-4da4-9c77-e8e92172fa88")

    monkeypatch.setattr(UserRepository, "get_uid_by_username", uid_provider)


@pytest.fixture
def login_patch(monkeypatch):
    def login_data_patch(uid):
        return {
                "result": {
                    "access": {
                        "token": "cca4eb1fa7a244d42895e1f1dd7f89253928b0e65db7d99e692e8f253778c3af",
                        "expire": "2021-12-29T10:24:35"
                    },
                    "refresh": {
                        "token": "f2301ecdc55a568264d9d7b32c0f1cf36719d1c72a409e1488090bd9fae6b180",
                        "expire": "2021-12-29T18:14:35"
                    }
                }
            }

    monkeypatch.setattr(UserAuthRepository, "login", login_data_patch)


@pytest.fixture
def access_token_not_valid_patch(monkeypatch):
    def always_none(access_token):
        return None

    monkeypatch.setattr(UserAuthRepository, "authenticated", always_none)


@pytest.fixture
def access_token_valid_patch(monkeypatch):
    def fake_uuid(access_token):
        return UUID("bd9213db-8d4c-4da4-9c77-e8e92172fa88")

    monkeypatch.setattr(UserAuthRepository, "authenticated", fake_uuid)


@pytest.fixture
def refresh_token_not_valid_patch(monkeypatch):
    def always_none(refresh_token):
        return None

    monkeypatch.setattr(UserAuthRepository, "refresh_access", always_none)


@pytest.fixture
def get_auth_data_patch(monkeypatch):
    def fake_access(uid):
        return {
                "result": {
                    "access": {
                        "token": "cca4eb1fa7a244d42895e1f1dd7f89253928b0e65db7d99e692e8f253778c3af",
                        "expire": "2021-12-29T10:24:35"
                    },
                    "refresh": {
                        "token": "f2301ecdc55a568264d9d7b32c0f1cf36719d1c72a409e1488090bd9fae6b180",
                        "expire": "2021-12-29T18:14:35"
                    }
                }
            }

    monkeypatch.setattr(UserAuthRepository, "get_authentication_data", fake_access)


@pytest.fixture
def refresh_token_valid_patch(monkeypatch):
    def fake_access(refresh_token):
        return {
                "result": {
                    "access": {
                        "token": "cca4eb1fa7a244d42895e1f1dd7f89253928b0e65db7d99e692e8f253778c3af",
                        "expire": "2021-12-29T10:24:35"
                    },
                    "refresh": {
                        "token": "f2301ecdc55a568264d9d7b32c0f1cf36719d1c72a409e1488090bd9fae6b180",
                        "expire": "2021-12-29T18:14:35"
                    }
                }
            }

    monkeypatch.setattr(UserAuthRepository, "refresh_access", fake_access)


@pytest.fixture
def logout_patch(monkeypatch):
    def always_none(uid):
        return None

    monkeypatch.setattr(UserAuthRepository, "logout", always_none)
