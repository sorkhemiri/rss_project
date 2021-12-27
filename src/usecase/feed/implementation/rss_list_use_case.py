import json
from typing import Type

from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from interfaces.feed_manager_repository_interface import FeedManagerRepositoryInterface
from interfaces.rss_repository_interface import RSSRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status


class RSSListUseCase(UseCaseInterface):
    def __init__(
            self,
            validator: Type[ValidatorInterface],
            rss_repository: Type[RSSRepositoryInterface],
            feed_manager_repository: Type[FeedManagerRepositoryInterface]
    ):
        self.validator = validator
        self.rss_repository = rss_repository
        self.feed_manager_repository = feed_manager_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            user = data.user
            page = data.page
            limit = data.limit
            user_feed = self.feed_manager_repository.get_feed(user_id=user.id, page=page, limit=limit)
            unseen_feed = self.feed_manager_repository.get_unseen(user_id=user.id)
            rss_ids = [int(item[0]) for item in user_feed]
            seen_posts = [item for item in unseen_feed if int(item) in rss_ids]
            self.feed_manager_repository.remove_from_unseen(user_id=user.id, post_ids=seen_posts)
            rss_list = self.rss_repository.get_list(rss_ids=rss_ids)
            rss_list_data = []
            for item in rss_list:
                item_data = item.dict(exclude_defaults=True)
                if item.pub_date:
                    item_data["pub_date"] = item.pub_date.timestamp()
                rss_list_data.append(item_data)
            return JSONResponse(content={"rss": rss_list_data, "unseen_rss": unseen_feed}, status_code=HTTP_200_OK)
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
