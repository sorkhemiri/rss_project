import json
from typing import Type

from pydantic import ValidationError

from interfaces.like_repository_interface import LikeRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException


class UserLikesListUseCase(UseCaseInterface):
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
            offset = data.offset
            limit = data.limit
            likes_data = self.like_repository.get_user_likes_list(
                user_id=user.id, offset=offset, limit=limit
            )
            likes_list = [item.dict(exclude_defaults=True) for item in likes_data]
            return {"likes": likes_list, "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
