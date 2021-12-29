import re
from uuid import UUID

import pytest

from entities import User
from repositories.postgres import UserRepository


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
