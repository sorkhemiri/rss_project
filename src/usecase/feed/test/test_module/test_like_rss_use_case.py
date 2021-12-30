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
