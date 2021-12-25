from uuid import uuid4
from typing import Type

import json
import jwt
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from interfaces.user_auth_repository_interface import UserAuthRepositoryInterface
from interfaces.user_repository_interface import UserRepositoryInterface
from interfaces.validator import ValidatorInterface
from settings import env_config
from usecase.interface import UseCaseInterface

from exceptions import UseCaseException, error_status


class LoginUseCase(UseCaseInterface):
    def __init__(
            self,
            validator: Type[ValidatorInterface],
            user_auth_repository: Type[UserAuthRepositoryInterface],
            user_repository: Type[UserRepositoryInterface],
    ):
        self.validator = validator
        self.user_auth_repository = user_auth_repository
        self.user_repository = user_repository

    def process_request(self, request_dict: dict):
        try:
            data = self.validator(**request_dict)
            username = data.username
            password = data.password
            if not self.user_repository.check_username_exist(username=username):
                raise UseCaseException(message="User not found", error_code=error_status.DOES_NOT_EXIST_ERROR)
            if not self.user_repository.check_password(username=username, password=password):
                raise UseCaseException(message="Password incorrect", error_code=error_status.DOES_NOT_EXIST_ERROR)
            user_id = self.user_repository.get_uid_by_username(username=username)
            result = self.user_auth_repository.login(uid=user_id)
            return {"result": result, "http_status_code": 200}
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
