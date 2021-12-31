import json
from typing import Type

from pydantic import ValidationError

from interfaces.feed_manager_repository_interface import FeedManagerRepositoryInterface
from interfaces.like_repository_interface import LikeRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException


class RemoveFromUnseenUseCase(UseCaseInterface):
    def __init__(
        self,
        validator: Type[ValidatorInterface],
        feed_manager_repository: Type[FeedManagerRepositoryInterface],
    ):
        self.validator = validator
        self.feed_manager_repository = feed_manager_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            user = data.user
            rss_data = data.rss_data
            all_rss_ids = []
            for item in rss_data:
                self.feed_manager_repository.remove_from_source_unseen(
                    user_id=user.id, post_ids=item.rss_ids, source_key=item.source_key
                )
                all_rss_ids.extend(item.rss_ids)
            self.feed_manager_repository.remove_from_unseen(
                user_id=user.id, post_ids=all_rss_ids
            )
            return {"result": "Items seen", "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
