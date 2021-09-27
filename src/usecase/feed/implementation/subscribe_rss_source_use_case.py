import orjson as json
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from entities import Subscription, RSSSource
from repositories.postgres import RSSSourceRepository
from repositories.postgres import SubscriptionRepository
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
            SubscriptionRepository.create(subscription=subscription)
            return JSONResponse(content={"result": "user subscribed successfully"}, status_code=HTTP_200_OK)
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
