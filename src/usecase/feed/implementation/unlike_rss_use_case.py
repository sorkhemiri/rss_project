import json
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from entities import Like, RSS
from repositories.postgres import LikeRepository
from usecase.interface import UseCaseInterface

from utils.exceptions import UseCaseException
from validators.feed import UnlikeRSSValidator


class UnlikeRSSUseCase(UseCaseInterface):
    def process_request(self, request_dict: dict):
        try:
            data = UnlikeRSSValidator(**request_dict)
            like = Like()
            like.user = data.user
            like.rss = RSS(id=data.rss_id)
            if LikeRepository.user_like_exist(model=like):
                LikeRepository.delete(model=like)
            return JSONResponse(content={"result": "rss unliked"}, status_code=HTTP_200_OK)
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
