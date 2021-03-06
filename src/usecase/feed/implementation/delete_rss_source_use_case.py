from typing import Type

import json
from pydantic import ValidationError

from interfaces.rss_source_repository_interface import RSSSourceRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status


class DeleteRSSSourceUseCase(UseCaseInterface):
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
            if not self.rss_source_repository.check_source_key_exists(key=data.key):
                raise UseCaseException(
                    message="Source not found",
                    error_code=error_status.DOES_NOT_EXIST_ERROR,
                )
            self.rss_source_repository.delete(key=data.key)
            return {"result": "Source deleted", "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
