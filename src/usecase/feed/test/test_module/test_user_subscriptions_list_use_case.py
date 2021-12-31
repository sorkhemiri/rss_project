from entities import User
from repositories.postgres import SubscriptionRepository
from usecase.feed.implementation import UserSubscriptionsListUseCase
from validators.feed import UserSubscriptionsListValidator


class UserSubscriptionsListUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = UserSubscriptionsListUseCase(
            validator=UserSubscriptionsListValidator,
            subscription_repository=SubscriptionRepository,
        )

        request_data = {}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_outcome(subscription_list_patch):
        use_case = UserSubscriptionsListUseCase(
            validator=UserSubscriptionsListValidator,
            subscription_repository=SubscriptionRepository,
        )

        request_data = {"user": User()}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["subscriptions"] == [
            {"source": {"key": "test_key1", "title": "test_title1"}},
            {"source": {"key": "test_key2", "title": "test_title2"}},
        ]
