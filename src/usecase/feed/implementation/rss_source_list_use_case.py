import json
from typing import Type

from pydantic import ValidationError

from interfaces.rss_source_repository_interface import RSSSourceRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException


class RSSSourceListUseCase(UseCaseInterface):
    def __init__(
        self,
        validator: Type[ValidatorInterface],
        rss_source_repository: Type[RSSSourceRepositoryInterface],
    ):
        self.validator = validator
        self.rss_source_repository = rss_source_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            offset = data.offset
            limit = data.limit
            rss_sources = self.rss_source_repository.get_list(
                offset=offset, limit=limit
            )
            rss_source_data = [item.dict(exclude_defaults=True) for item in rss_sources]
            return {"rss_sources": rss_source_data, "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
