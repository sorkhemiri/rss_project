import json
from typing import Type

from pydantic import ValidationError

from interfaces.feed_manager_repository_interface import FeedManagerRepositoryInterface
from interfaces.rss_repository_interface import RSSRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException


class GetRSSSourceFeedUseCase(UseCaseInterface):
    def __init__(
        self,
        validator: Type[ValidatorInterface],
        rss_repository: Type[RSSRepositoryInterface],
        feed_manager_repository: Type[FeedManagerRepositoryInterface],
    ):
        self.validator = validator
        self.rss_repository = rss_repository
        self.feed_manager_repository = feed_manager_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            source_key = data.source_key
            page = data.page
            limit = data.limit
            user = data.user
            source_feed = self.feed_manager_repository.get_channel(
                key=source_key, page=page, limit=limit
            )
            rss_ids = [int(item[0]) for item in source_feed]
            rss_list = self.rss_repository.get_list(rss_ids=rss_ids)
            unseen_rss_ids = self.feed_manager_repository.get_source_unseen(
                user_id=user.id, source_key=source_key
            )
            unseen_rss_list = self.rss_repository.get_list(rss_ids=unseen_rss_ids)
            rss_list_data = []
            for item in rss_list:
                item_data = item.dict(exclude_defaults=True)
                rss_list_data.append(item_data)

            unseen_rss_data = []
            for item in unseen_rss_list:
                item_data = item.dict(exclude_defaults=True)
                unseen_rss_data.append(item_data)
            return {
                "rss": rss_list_data,
                "unseen": unseen_rss_data,
                "http_status_code": 200,
            }
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
