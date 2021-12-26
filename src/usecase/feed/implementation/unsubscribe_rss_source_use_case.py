import json
from typing import Type

from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from entities import Subscription, RSSSource
from interfaces.rss_source_repository_interface import RSSSourceRepositoryInterface
from interfaces.subscription_repository_interface import SubscriptionRepositoryInterface
from interfaces.validator import ValidatorInterface
from repositories.postgres import RSSSourceRepository
from repositories.postgres import SubscriptionRepository
from repositories.redis import FeedManager
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status
from validators.feed import UnsubscribeRSSSourceValidator


class UnsubscribeRSSSourceUseCase(UseCaseInterface):
    def __init__(
            self,
            validator: Type[ValidatorInterface],
            rss_source_repository: Type[RSSSourceRepositoryInterface],
            subscription_repository: Type[SubscriptionRepositoryInterface]
    ):
        self.validator = validator
        self.rss_source_repository = rss_source_repository
        self.subscription_repository = subscription_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            source_key = data.source_key
            user = data.user
            if not self.rss_source_repository.check_source_key_exists(key=source_key):
                raise UseCaseException(message="source not found", error_code=error_status.DOES_NOT_EXIST_ERROR)
            source_id = self.rss_source_repository.get_sources_id_by_key(source_key=source_key)
            subscription = Subscription()
            subscription.user = user
            subscription.source = RSSSource(id=source_id)
            SubscriptionRepository.delete(model=subscription)
            values = FeedManager.get_channel_all(key=source_key)
            rss_ids = [item[0] for item in values]
            FeedManager.delete_from_feed(user_id=user.id, values=rss_ids)
            return {"result": "user unsubscribed successfully", "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
