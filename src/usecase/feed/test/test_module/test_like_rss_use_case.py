from entities import User
from repositories.postgres import LikeRepository
from usecase.feed.implementation import LikeRSSUseCase
from validators.feed import LikeRSSValidator


class LikeRSSUseCaseTestCase:

    @staticmethod
    def test_input():
        use_case = LikeRSSUseCase(
            validator=LikeRSSValidator, like_repository=LikeRepository
        )

        request_data = {"rss_id": 1}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_like_exist(like_exist_patch):
        use_case = LikeRSSUseCase(
            validator=LikeRSSValidator, like_repository=LikeRepository
        )

        request_data = {"rss_id": 1, "user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == "rss liked"

    @staticmethod
    def test_like_not_exist(like_not_exist_patch, like_create_patch):
        use_case = LikeRSSUseCase(
            validator=LikeRSSValidator, like_repository=LikeRepository
        )

        request_data = {"rss_id": 1, "user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == "rss liked"
