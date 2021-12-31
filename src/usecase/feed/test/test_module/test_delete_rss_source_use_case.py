from repositories.postgres import RSSSourceRepository
from usecase.feed.implementation import DeleteRSSSourceUseCase
from validators.feed import DeleteRSSSourceValidator


class DeleteRSSSourceUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = DeleteRSSSourceUseCase(
            validator=DeleteRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_key_not_exist(key_not_exist_patch):
        use_case = DeleteRSSSourceUseCase(
            validator=DeleteRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {"key": "some_key"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 404
        assert data["type"] == "DOES NOT EXIST ERROR"
        assert data["message"] == "Source not found"

    @staticmethod
    def test_outcome(key_exist_patch, delete_source_patch):
        use_case = DeleteRSSSourceUseCase(
            validator=DeleteRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {"key": "some_key"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == "Source deleted"
