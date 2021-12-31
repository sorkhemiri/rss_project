from repositories.postgres import RSSSourceRepository
from usecase.feed.implementation import RSSSourceListUseCase
from validators.feed import RSSSourceListValidator


class RSSSourceListUseCaseTestCase:
    @staticmethod
    def test_outcome(rss_source_list_patch):
        use_case = RSSSourceListUseCase(
            validator=RSSSourceListValidator, rss_source_repository=RSSSourceRepository
        )

        request_data = {}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["rss_sources"] == [
            {
                "key": "test_key1",
                "title": "test_title1",
                "description": "test_description1",
                "link": "test_link1",
            },
            {
                "key": "test_key2",
                "title": "test_title2",
                "description": "test_description2",
                "link": "test_link2",
            },
        ]
