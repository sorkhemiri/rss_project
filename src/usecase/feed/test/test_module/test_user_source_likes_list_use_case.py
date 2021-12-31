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

    @staticmethod
    def test_source_not_exist(key_not_exist_patch):
        use_case = UserSourceLikesListUseCase(
            validator=UserSourceLikesListValidator,
            like_repository=LikeRepository,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {"user": User(), "source_key": "some_key"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 404
        assert data["type"] == "DOES NOT EXIST ERROR"
        assert data["message"] == "Source not found"

    @staticmethod
    def test_outcome(key_exist_patch, source_id_by_key_patch, source_like_list_patch):
        use_case = UserSourceLikesListUseCase(
            validator=UserSourceLikesListValidator,
            like_repository=LikeRepository,
            rss_source_repository=RSSSourceRepository,
        )

        request_data = {"user": User(), "source_key": "some_key"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["likes"] == [
            {"rss": {"id": 1, "title": "test_title1"}},
            {"rss": {"id": 2, "title": "test_title2"}},
        ]
