from re import fullmatch

import json
from typing import Type

from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from entities import User
from interfaces.validator import ValidatorInterface
from interfaces.user_repository_interface import UserRepositoryInterface
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status


class RegisterUseCase(UseCaseInterface):
    def __init__(
        self,
        validator: Type[ValidatorInterface],
        user_repository: Type[UserRepositoryInterface],
    ):
        self.validator = validator
        self.user_repository = user_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            username = data.username
            first_name = data.first_name
            last_name = data.last_name
            password = data.password
            if self.user_repository.check_username_exist(username=username):
                raise UseCaseException(
                    message="username already exists",
                    error_code=error_status.VALIDATION_ERROR,
                )
            if not fullmatch(pattern="[a-zA-Z0-9_]{4,}", string=username):
                raise UseCaseException(
                    message="username not valid",
                    error_code=error_status.VALIDATION_ERROR,
                )
            user = User()
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.password = password
            created_user = self.user_repository.create(model=user)
            return {
                "user": created_user.dict(exclude_defaults=True),
                "http_status_code": 200,
            }
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
