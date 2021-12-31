from repositories.postgres import UserRepository, RSSSourceRepository
from repositories.redis import UserAuthRepository
from usecase.account.implementation import LoginUseCase
from usecase.feed.implementation import CreateRSSSourceUseCase
from validators.account import LoginValidator
from validators.feed import CreateRSSSourceValidator


class CreateRSSSourceUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = CreateRSSSourceUseCase(
            validator=CreateRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {"title": "some_title", "link": "some_link"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"key": "some_key", "link": "some_link"}
        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"key": "some_key", "title": "some_title"}
        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"key": "some_key", "title": "", "link": "some_link"}
        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
        assert data["message"] == "title must not be empty"

        request_data = {"key": "some_key", "title": "some_title", "link": ""}
        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
        assert data["message"] == "link must not be empty"

    @staticmethod
    def test_key_not_valid():
        use_case = CreateRSSSourceUseCase(
            validator=CreateRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {
            "key": "invalid*key",
            "title": "some_title",
            "link": "some_link",
        }

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
        assert data["message"] == "key not valid"

    @staticmethod
    def test_key_already_exist(key_exist_patch):
        use_case = CreateRSSSourceUseCase(
            validator=CreateRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {"key": "valid_key", "title": "some_title", "link": "some_link"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
        assert data["message"] == "Source key already exists"

    @staticmethod
    def test_outcome(key_not_exist_patch, create_source_patch):
        use_case = CreateRSSSourceUseCase(
            validator=CreateRSSSourceValidator,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {"key": "ValidKey", "title": "some_title", "link": "some_link"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["source"] == {
            "key": "validkey",
            "title": "some_title",
            "link": "some_link",
        }
