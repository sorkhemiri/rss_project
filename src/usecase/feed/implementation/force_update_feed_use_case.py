from typing import Type

import json
from pydantic import ValidationError

from interfaces.rss_source_repository_interface import RSSSourceRepositoryInterface
from interfaces.validator import ValidatorInterface
from jobs.add_from_stream import inner_function
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status


class ForceUpdateFeedUseCase(UseCaseInterface):
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
            key = data.source_key
            if not self.rss_source_repository.check_source_key_exists(key=key):
                raise UseCaseException(
                    message="Source not found",
                    error_code=error_status.DOES_NOT_EXIST_ERROR,
                )
            self.rss_source_repository.unmake_update_need(source_key=key)
            source = self.rss_source_repository.get_source_by_key(source_key=key)
            if inner_function(source=source):
                return {"result": "Feed updated", "http_status_code": 200}
            else:
                return {"result": "Feed update failed", "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
