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
