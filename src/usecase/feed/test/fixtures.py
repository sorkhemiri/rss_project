import re
from uuid import UUID

import pytest

from entities import User, RSSSource
from repositories.postgres import RSSSourceRepository
from repositories.redis import UserAuthRepository


@pytest.fixture
def key_exist_patch(monkeypatch):
    def always_true(key):
        return True

    monkeypatch.setattr(RSSSourceRepository, "check_source_key_exists", always_true)


@pytest.fixture
def key_not_exist_patch(monkeypatch):
    def always_false(key):
        return False

    monkeypatch.setattr(RSSSourceRepository, "check_source_key_exists", always_false)


@pytest.fixture
def create_source_patch(monkeypatch):
    def rss_source_patch(model: RSSSource):
        return model

    monkeypatch.setattr(RSSSourceRepository, "create", rss_source_patch)


@pytest.fixture
def delete_source_patch(monkeypatch):
    def always_none(key):
        return None

    monkeypatch.setattr(RSSSourceRepository, "delete", always_none)
