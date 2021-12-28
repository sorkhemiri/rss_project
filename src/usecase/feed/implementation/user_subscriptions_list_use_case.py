import json
from typing import Type

from pydantic import ValidationError

from interfaces.subscription_repository_interface import SubscriptionRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status


class UserSubscriptionsListUseCase(UseCaseInterface):
    def __init__(
        self,
        validator: Type[ValidatorInterface],
        subscription_repository: Type[SubscriptionRepositoryInterface],
    ):
        self.validator = validator
        self.subscription_repository = subscription_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            user = data.user
            offset = data.offset
            limit = data.limit
            subscriptions_data = (
                self.subscription_repository.get_user_subscriptions_list(
                    user_id=user.id, offset=offset, limit=limit
                )
            )
            subscriptions_list = [
                item.dict(exclude_defaults=True) for item in subscriptions_data
            ]
            return {"subscriptions": subscriptions_list, "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
