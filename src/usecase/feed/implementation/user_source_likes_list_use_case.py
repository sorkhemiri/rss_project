import json
from typing import Type

from pydantic import ValidationError

from interfaces.like_repository_interface import LikeRepositoryInterface
from interfaces.rss_source_repository_interface import RSSSourceRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status


class UserSourceLikesListUseCase(UseCaseInterface):
    def __init__(
        self,
        validator: Type[ValidatorInterface],
        like_repository: Type[LikeRepositoryInterface],
        rss_source_repository: Type[RSSSourceRepositoryInterface],
    ):
        self.validator = validator
        self.like_repository = like_repository
        self.rss_source_repository = rss_source_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            user = data.user
            offset = data.offset
            limit = data.limit
            source_key = data.source_key
            if not self.rss_source_repository.check_source_key_exists(key=source_key):
                raise UseCaseException(
                    message="Source not found",
                    error_code=error_status.DOES_NOT_EXIST_ERROR,
                )

            source_id = self.rss_source_repository.get_sources_id_by_key(
                source_key=source_key
            )
            likes_data = self.like_repository.get_user_source_likes_list(
                user_id=user.id, offset=offset, limit=limit, source_id=source_id
            )
            likes_list = [item.dict(exclude_defaults=True) for item in likes_data]
            return {"likes": likes_list, "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
