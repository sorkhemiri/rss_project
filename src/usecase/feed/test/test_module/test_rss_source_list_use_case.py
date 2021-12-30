from repositories.postgres import RSSSourceRepository
from usecase.feed.implementation import RSSSourceListUseCase
from validators.feed import RSSSourceListValidator


class RSSSourceListUseCaseTestCase:

    @staticmethod
    def test_input():
        pass
        # use_case = RSSSourceListUseCase(
        #     validator=RSSSourceListValidator, rss_source_repository=RSSSourceRepository
        # )
        #
        # request_data = {}
        #
        # data = use_case.execute(request_model=request_data or {})
        # assert data["http_status_code"] == 400
        # assert data["type"] == "VALIDATION ERROR"
