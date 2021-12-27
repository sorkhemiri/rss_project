import json
from typing import Type

from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from entities import Like, RSS
from interfaces.like_repository_interface import LikeRepositoryInterface
from interfaces.validator import ValidatorInterface
from repositories.postgres import LikeRepository
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException
from validators.feed import LikeRSSValidator


class LikeRSSUseCase(UseCaseInterface):
    def __init__(
            self,
            validator: Type[ValidatorInterface],
            like_repository: Type[LikeRepositoryInterface],
    ):
        self.validator = validator
        self.like_repository = like_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            user = data.user
            rss_id = data.rss_id
            like = Like()
            like.user = user
            like.rss = RSS(id=rss_id)
            if not self.like_repository.user_like_exist(model=like):
                self.like_repository.create(model=like)
            return {"result": "rss liked", "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
