from entities import User
from repositories.redis import FeedManagerRepository
from usecase.feed.implementation import RemoveFromUnseenUseCase
from validators.feed import RemoveFromUnseenValidator


class RemoveFromUnseenUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = RemoveFromUnseenUseCase(
            validator=RemoveFromUnseenValidator,
            feed_manager_repository=FeedManagerRepository,
        )

        request_data = {"user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"user": User(), "rss_data": [{"source_key": "some_key"}]}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"user": User(), "rss_data": [{"rss_ids": [1, 2, 3]}]}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"rss_data": [{"source_key": "some_key", "rss_ids": [1, 2, 3]}]}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_outcome(remove_from_unseen_patch, remove_from_source_unseen_patch):
        use_case = RemoveFromUnseenUseCase(
            validator=RemoveFromUnseenValidator,
            feed_manager_repository=FeedManagerRepository,
        )
        request_data = {
            "user": User(),
            "rss_data": [{"source_key": "some_key", "rss_ids": [1, 2, 3]}],
        }

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == "Items seen"
