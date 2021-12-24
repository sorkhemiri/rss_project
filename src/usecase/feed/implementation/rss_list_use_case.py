import json
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from repositories.postgres import RSSRepository
from repositories.redis import FeedManager
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status
from validators.feed import RSSListValidator


class RSSListUseCase(UseCaseInterface):
    def process_request(self, request_dict: dict):
        try:
            data = RSSListValidator(**request_dict)
            user_feed = FeedManager.get_feed(user_id=data.user.id, page=data.page, limit=data.limit)
            unseen_feed = FeedManager.get_unseen(user_id=data.user.id)
            rss_ids = [int(item[0]) for item in user_feed]
            seen_posts = [item for item in unseen_feed if int(item) in rss_ids]
            FeedManager.remove_from_unseen(user_id=data.user.id, post_ids=seen_posts)
            rss_list = RSSRepository.get_list(rss_ids=rss_ids)
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
