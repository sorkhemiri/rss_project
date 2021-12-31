import json
from typing import Type

from pydantic import ValidationError

from entities import Subscription, RSSSource
from interfaces.feed_manager_repository_interface import FeedManagerRepositoryInterface
from interfaces.rss_source_repository_interface import RSSSourceRepositoryInterface
from interfaces.subscription_repository_interface import SubscriptionRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status


class UnsubscribeRSSSourceUseCase(UseCaseInterface):
    def __init__(
        self,
        validator: Type[ValidatorInterface],
        rss_source_repository: Type[RSSSourceRepositoryInterface],
        subscription_repository: Type[SubscriptionRepositoryInterface],
        feed_manager_repository: Type[FeedManagerRepositoryInterface],
    ):
        self.validator = validator
        self.rss_source_repository = rss_source_repository
        self.subscription_repository = subscription_repository
        self.feed_manager_repository = feed_manager_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            source_key = data.source_key
            user = data.user
            if not self.rss_source_repository.check_source_key_exists(key=source_key):
                raise UseCaseException(
                    message="Source not found",
                    error_code=error_status.DOES_NOT_EXIST_ERROR,
                )
            source_id = self.rss_source_repository.get_sources_id_by_key(
                source_key=source_key
            )
            subscription = Subscription()
            subscription.user = user
            subscription.source = RSSSource(id=source_id)
            self.subscription_repository.delete(model=subscription)
            values = self.feed_manager_repository.get_channel_all(key=source_key)
            rss_ids = [item[0] for item in values]
            self.feed_manager_repository.delete_from_feed(
                user_id=user.id, values=rss_ids
            )
            return {"result": "User unsubscribed successfully", "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
