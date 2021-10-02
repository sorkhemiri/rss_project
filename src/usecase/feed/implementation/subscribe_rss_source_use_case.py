import json
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from entities import Subscription, RSSSource
from repositories.postgres import RSSSourceRepository
from repositories.postgres import SubscriptionRepository
from repositories.redis import FeedManager
from usecase.interface import UseCaseInterface

from utils.exceptions import UseCaseException, status
from validators.feed import SubscribeRSSSourceValidator


class SubscribeRSSSourceUseCase(UseCaseInterface):
    def process_request(self, request_dict: dict):
        try:
            data = SubscribeRSSSourceValidator(**request_dict)
            if not RSSSourceRepository.check_source_exists(data.source_id):
                raise UseCaseException(message="source not found", error_code=status.DOES_NOT_EXIST_ERROR)
            subscription = Subscription()
            subscription.user = data.user
            subscription.source = RSSSource(id=data.source_id)
            if not SubscriptionRepository.check_subscription_exist(model=subscription):
                SubscriptionRepository.create(model=subscription)
                source_key = RSSSourceRepository.get_sources_key(source_id=data.source_id)
                values = FeedManager.get_channel(key=source_key, page=1, limit=1000)
                FeedManager.add_to_feed(user_id=data.user.id, feed=values)
            return JSONResponse(content={"result": "user subscribed successfully"}, status_code=HTTP_200_OK)
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
