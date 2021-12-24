import json
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from entities import Like, RSS
from repositories.postgres import LikeRepository
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException
from validators.feed import LikeRSSValidator


class LikeRSSUseCase(UseCaseInterface):
    def process_request(self, request_dict: dict):
        try:
            data = LikeRSSValidator(**request_dict)
            like = Like()
            like.user = data.user
            like.rss = RSS(id=data.rss_id)
            if not LikeRepository.user_like_exist(model=like):
                LikeRepository.create(model=like)
            return JSONResponse(content={"result": "rss liked"}, status_code=HTTP_200_OK)
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
