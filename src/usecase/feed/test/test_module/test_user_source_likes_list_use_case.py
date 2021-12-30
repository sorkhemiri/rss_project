from entities import User
from repositories.postgres import LikeRepository, RSSSourceRepository
from usecase.feed.implementation import UserSourceLikesListUseCase
from validators.feed import UserSourceLikesListValidator


class UserSourceLikesListUseCaseTestCase:

    @staticmethod
    def test_input():
        use_case = UserSourceLikesListUseCase(
            validator=UserSourceLikesListValidator,
            like_repository=LikeRepository,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {"user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"source_key": "some_key"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
