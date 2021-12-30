import re
from datetime import datetime
from uuid import UUID

import pytest

from entities import User, RSSSource, RSS
from repositories.postgres import RSSSourceRepository, RSSRepository
from repositories.redis import UserAuthRepository, FeedManagerRepository


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


@pytest.fixture
def get_channel_patch(monkeypatch):
    def fake_ids(key, page, limit):
        return [("1", "1111111"), ("2", "22222222")]

    monkeypatch.setattr(FeedManagerRepository, "get_channel", fake_ids)


@pytest.fixture
def get_rss_list_patch(monkeypatch):
    def fake_rss(rss_ids):
        return [
            RSS(
                id=1,
                title="test_title1",
                link="test_link1",
                description="test description1",
                source=RSSSource(id=1),
                pub_date=datetime(year=2021, month=1, day=1)),
            RSS(
                id=2,
                title="test_title2",
                link="test_link2",
                description="test description2",
                source=RSSSource(id=2),
                pub_date=datetime(year=2021, month=1, day=2)),
        ]

    monkeypatch.setattr(RSSRepository, "get_list", fake_rss)


@pytest.fixture
def source_unseen_patch(monkeypatch):
    def fake_ids(user_id, source_key):
        return ["1", "2"]

    monkeypatch.setattr(FeedManagerRepository, "get_source_unseen", fake_ids)
