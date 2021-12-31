import re
from datetime import datetime
from uuid import UUID

import pytest

from entities import User, RSSSource, RSS
from repositories.postgres import (
    RSSSourceRepository,
    RSSRepository,
    LikeRepository,
    SubscriptionRepository,
)
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
                pub_date=datetime(year=2021, month=1, day=1),
            ),
            RSS(
                id=2,
                title="test_title2",
                link="test_link2",
                description="test description2",
                source=RSSSource(id=2),
                pub_date=datetime(year=2021, month=1, day=2),
            ),
        ]

    monkeypatch.setattr(RSSRepository, "get_list", fake_rss)


@pytest.fixture
def source_unseen_patch(monkeypatch):
    def fake_ids(user_id, source_key):
        return ["1", "2"]

    monkeypatch.setattr(FeedManagerRepository, "get_source_unseen", fake_ids)


@pytest.fixture
def like_exist_patch(monkeypatch):
    def always_true(model):
        return True

    monkeypatch.setattr(LikeRepository, "user_like_exist", always_true)


@pytest.fixture
def like_not_exist_patch(monkeypatch):
    def always_false(model):
        return False

    monkeypatch.setattr(LikeRepository, "user_like_exist", always_false)


@pytest.fixture
def like_create_patch(monkeypatch):
    def fake_like_create(model):
        return None

    monkeypatch.setattr(LikeRepository, "create", fake_like_create)


@pytest.fixture
def rss_source_list_patch(monkeypatch):
    def fake_rss_source_list(offset, limit):
        return [
            RSSSource(
                title="test_title1",
                key="test_key1",
                description="test_description1",
                link="test_link1",
            ),
            RSSSource(
                title="test_title2",
                key="test_key2",
                description="test_description2",
                link="test_link2",
            ),
        ]

    monkeypatch.setattr(RSSSourceRepository, "get_list", fake_rss_source_list)


@pytest.fixture
def source_id_by_key_patch(monkeypatch):
    def fake_id(source_key):
        return 1

    monkeypatch.setattr(RSSSourceRepository, "get_sources_id_by_key", fake_id)


@pytest.fixture
def subscription_exist_patch(monkeypatch):
    def always_true(model):
        return True

    monkeypatch.setattr(SubscriptionRepository, "check_subscription_exist", always_true)


@pytest.fixture
def subscription_not_exist_patch(monkeypatch):
    def always_false(model):
        return False

    monkeypatch.setattr(
        SubscriptionRepository, "check_subscription_exist", always_false
    )


@pytest.fixture
def subscription_create_patch(monkeypatch):
    def fake_create(model):
        return None

    monkeypatch.setattr(SubscriptionRepository, "create", fake_create)


@pytest.fixture
def delete_like_patch(monkeypatch):
    def fake_delete(model):
        return None

    monkeypatch.setattr(LikeRepository, "delete", fake_delete)


@pytest.fixture
def delete_subscription_patch(monkeypatch):
    def fake_delete(model):
        return None

    monkeypatch.setattr(SubscriptionRepository, "delete", fake_delete)


@pytest.fixture
def get_channel_all_patch(monkeypatch):
    def fake_get(key):
        return [("1", "1111111"), ("2", "22222222")]

    monkeypatch.setattr(FeedManagerRepository, "get_channel_all", fake_get)


@pytest.fixture
def delete_from_feed(monkeypatch):
    def always_none(user_id, values):
        return None

    monkeypatch.setattr(FeedManagerRepository, "delete_from_feed", always_none)


@pytest.fixture
def user_feed_patch(monkeypatch):
    def fake_feed(user_id, page, limit):
        return [("1", "1111111"), ("2", "22222222")]

    monkeypatch.setattr(FeedManagerRepository, "get_feed", fake_feed)


@pytest.fixture
def unseen_rss_ids_patch(monkeypatch):
    def fake_ids(user_id):
        return ["1", "2"]

    monkeypatch.setattr(FeedManagerRepository, "get_unseen", fake_ids)
