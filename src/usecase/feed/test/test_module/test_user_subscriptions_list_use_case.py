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
