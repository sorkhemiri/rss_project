from entities import User
from repositories.postgres import LikeRepository
from usecase.feed.implementation import UserLikesListUseCase
from validators.feed import UserLikesListValidator


class UserLikesListUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = UserLikesListUseCase(
            validator=UserLikesListValidator, like_repository=LikeRepository
        )

        request_data = {}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_outcome(like_list_patch):
        use_case = UserLikesListUseCase(
            validator=UserLikesListValidator, like_repository=LikeRepository
        )

        request_data = {"user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["likes"] == [
            {"rss": {"id": 1, "title": "test_title1"}},
            {"rss": {"id": 2, "title": "test_title2"}},
        ]
