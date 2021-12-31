from entities import User
from repositories.postgres import RSSRepository
from repositories.redis import FeedManagerRepository
from usecase.feed.implementation import GetRSSSourceFeedUseCase
from validators.feed import GetRSSSourceFeedValidator


class GetRSSSourceFeedUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = GetRSSSourceFeedUseCase(
            validator=GetRSSSourceFeedValidator,
            rss_repository=RSSRepository,
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
    def test_outcome(get_channel_patch, get_rss_list_patch, source_unseen_patch):
        use_case = GetRSSSourceFeedUseCase(
            validator=GetRSSSourceFeedValidator,
            rss_repository=RSSRepository,
            feed_manager_repository=FeedManagerRepository,
        )

        request_data = {"source_key": "some_key", "user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["rss"] == [
            {
                "id": 1,
                "title": "test_title1",
                "link": "test_link1",
                "description": "test description1",
                "source": {"id": 1},
                "pub_date": "2021-01-01",
            },
            {
                "id": 2,
                "title": "test_title2",
                "link": "test_link2",
                "description": "test description2",
                "source": {"id": 2},
                "pub_date": "2021-01-02",
            },
        ]
        assert data["unseen"] == [
            {
                "id": 1,
                "title": "test_title1",
                "link": "test_link1",
                "description": "test description1",
                "source": {"id": 1},
                "pub_date": "2021-01-01",
            },
            {
                "id": 2,
                "title": "test_title2",
                "link": "test_link2",
                "description": "test description2",
                "source": {"id": 2},
                "pub_date": "2021-01-02",
            },
        ]
