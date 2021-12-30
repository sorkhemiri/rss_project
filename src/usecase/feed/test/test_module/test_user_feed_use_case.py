from repositories.postgres import RSSRepository
from repositories.redis import FeedManagerRepository
from usecase.feed.implementation import UserFeedUseCase
from validators.feed import UserFeedValidator


class UserFeedUseCaseTestCase:

    @staticmethod
    def test_input():
        use_case = UserFeedUseCase(
            validator=UserFeedValidator,
            rss_repository=RSSRepository,
            feed_manager_repository=FeedManagerRepository,
        )

        request_data = {}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
