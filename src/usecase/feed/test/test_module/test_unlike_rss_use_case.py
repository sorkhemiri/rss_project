from entities import User
from repositories.postgres import LikeRepository
from usecase.feed.implementation import UnlikeRSSUseCase
from validators.feed import UnlikeRSSValidator


class UnlikeRSSUseCaseTestCase:

    @staticmethod
    def test_input():
        use_case = UnlikeRSSUseCase(
            validator=UnlikeRSSValidator, like_repository=LikeRepository
        )

        request_data = {"rss_id": 1}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
