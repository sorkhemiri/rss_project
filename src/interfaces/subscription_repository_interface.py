import abc
from typing import List

from entities import Subscription
from .repository import RepositoryInterface


class SubscriptionRepositoryInterface(RepositoryInterface):
    """
    Subscription table related functionality
    """
    @classmethod
    @abc.abstractmethod
    def create(cls, model: Subscription) -> Subscription:
        pass

    @classmethod
    @abc.abstractmethod
    def delete(cls, model: Subscription):
        pass

    @classmethod
    @abc.abstractmethod
    def get_channel_subscriber_by_key(cls, key) -> List[Subscription]:
        pass

    @classmethod
    @abc.abstractmethod
    def check_subscription_exist(cls, model: Subscription) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def get_user_subscriptions_list(cls, user_id: int, offset: int = 0, limit: int = 10) -> List[Subscription]:
        pass
