from repositories.postgres import RSSSourceRepository
from usecase.feed.implementation import CreateRSSSourceUseCase, ForceUpdateFeedUseCase
from validators.feed import CreateRSSSourceValidator, ForceUpdateFeedValidator


class ForceUpdateFeedUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = ForceUpdateFeedUseCase(
            validator=ForceUpdateFeedValidator, rss_source_repository=RSSSourceRepository
        )

        request_data = {}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_source_not_exist(key_not_exist_patch):
        use_case = ForceUpdateFeedUseCase(
            validator=ForceUpdateFeedValidator, rss_source_repository=RSSSourceRepository
        )

        request_data = {
            "source_key": "some_key",
        }

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 404
        assert data["type"] == "DOES NOT EXIST ERROR"
        assert data["message"] == "Source not found"

