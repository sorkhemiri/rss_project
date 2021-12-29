from re import fullmatch
from typing import Type

import json
from pydantic import ValidationError

from entities import RSSSource
from interfaces.rss_source_repository_interface import RSSSourceRepositoryInterface
from interfaces.validator import ValidatorInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status


class CreateRSSSourceUseCase(UseCaseInterface):
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
            key = data.key
            title = data.title
            description = data.description
            link = data.link
            if not fullmatch(pattern="[a-zA-Z0-9_]{3,}", string=key):
                raise UseCaseException(
                    message="key not valid",
                    error_code=error_status.VALIDATION_ERROR,
                )

            key = key.lower()
            if self.rss_source_repository.check_source_key_exists(key=key):
                raise UseCaseException(
                    message="Source key already exists",
                    error_code=error_status.VALIDATION_ERROR,
                )
            source = RSSSource(
                key=key,
                title=title,
                description=description,
                link=link,
            )
            self.rss_source_repository.create(model=source)
            return {
                "source": source.dict(exclude_defaults=True),
                "http_status_code": 200,
            }
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
