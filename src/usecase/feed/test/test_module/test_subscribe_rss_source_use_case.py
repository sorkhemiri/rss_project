from entities import User
from repositories.postgres import RSSSourceRepository, SubscriptionRepository
from repositories.redis import FeedManagerRepository
from usecase.feed.implementation import SubscribeRSSSourceUseCase
from validators.feed import SubscribeRSSSourceValidator


class SubscribeRSSSourceUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = SubscribeRSSSourceUseCase(
            validator=SubscribeRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
            subscription_repository=SubscriptionRepository,
            feed_manager_repository=FeedManagerRepository,
        )

        request_data = {"user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"source_key": "some_key"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_source_not_exist(key_not_exist_patch):
        use_case = SubscribeRSSSourceUseCase(
            validator=SubscribeRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
            subscription_repository=SubscriptionRepository,
            feed_manager_repository=FeedManagerRepository,
        )

        request_data = {"user": User(), "source_key": "some_key"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 404
        assert data["type"] == "DOES NOT EXIST ERROR"
        assert data["message"] == "Source not found"

    @staticmethod
    def test_subscription_exist(
        key_exist_patch, source_id_by_key_patch, subscription_exist_patch
    ):
        use_case = SubscribeRSSSourceUseCase(
            validator=SubscribeRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
            subscription_repository=SubscriptionRepository,
            feed_manager_repository=FeedManagerRepository,
        )

        request_data = {"user": User(), "source_key": "some_key"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == "User subscribed successfully"

    @staticmethod
    def test_subscription_not_exist(
        key_exist_patch,
        source_id_by_key_patch,
        subscription_not_exist_patch,
        subscription_create_patch,
        get_channel_patch,
        add_to_feed_patch,
    ):
        use_case = SubscribeRSSSourceUseCase(
            validator=SubscribeRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
            subscription_repository=SubscriptionRepository,
            feed_manager_repository=FeedManagerRepository,
        )

        request_data = {"user": User(), "source_key": "some_key"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == "User subscribed successfully"
