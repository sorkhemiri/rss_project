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
