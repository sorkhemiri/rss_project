from uuid import uuid4
from typing import Type

import json
import jwt
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from entities import RSSSource
from interfaces.rss_source_repository_interface import RSSSourceRepositoryInterface
from interfaces.user_repository_interface import UserRepositoryInterface
from interfaces.validator import ValidatorInterface
from settings import env_config
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
            source = RSSSource(
                key=data.key,
                title=data.title,
                description=data.description,
                link=data.link,
            )
            if self.rss_source_repository.check_source_key_exists(key=source.key):
                raise UseCaseException(
                    message="Source key already exists",
                    error_code=error_status.VALIDATION_ERROR,
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
