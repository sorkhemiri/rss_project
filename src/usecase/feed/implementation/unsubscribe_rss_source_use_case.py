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
from validators.feed import UnsubscribeRSSSourceValidator


class UnsubscribeRSSSourceUseCase(UseCaseInterface):
    def process_request(self, request_dict: dict):
        try:
            data = UnsubscribeRSSSourceValidator(**request_dict)
            if not RSSSourceRepository.check_source_exists(data.source_id):
                raise UseCaseException(message="source not found", error_code=status.DOES_NOT_EXIST_ERROR)
            subscription = Subscription()
            subscription.user = data.user
            subscription.source = RSSSource(id=data.source_id)
            SubscriptionRepository.delete(model=subscription)
            source_key = RSSSourceRepository.get_sources_key(source_id=data.source_id)
            values = FeedManager.get_channel_all(key=source_key)
            rss_ids = [item[0] for item in values]
            FeedManager.delete_from_feed(user_id=data.user.id, values=rss_ids)
            return JSONResponse(content={"result": "user unsubscribed successfully"}, status_code=HTTP_200_OK)
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
