from json import loads
from typing import Type

from pydantic import ValidationError

from exceptions import error_status
from interfaces.use_case import UseCaseInterface
from interfaces.validator import ValidatorInterface
from interfaces.user_auth_repository_interface import UserAuthRepositoryInterface
from exceptions import UseCaseException


class RefreshAccessUseCase(UseCaseInterface):
    def __init__(
            self,
            validator: Type[ValidatorInterface],
            user_auth_repository: Type[UserAuthRepositoryInterface],
    ):
        self.validator = validator
        self.user_auth_repository = user_auth_repository

    def process_request(self, request_dict: dict):
        try:
            request_data = self.validator(**request_dict)
            uid = self.user_auth_repository.authenticated(access_token=request_data.access_token)
            if uid:
                authentication_data = self.user_auth_repository.get_authentication_data(uid=uid)
                response_data = {
                    "result": authentication_data,
                    "http_status_code": 200
                }

            else:
                authentication_data = self.user_auth_repository.refresh_access(refresh_token=request_data.refresh_token)
                if not authentication_data:
                    response_data = {
                        "result": "refresh token invalid or expired",
                        "http_status_code": 400
                    }
                else:
                    response_data = {
                        "result": authentication_data,
                        "http_status_code": 200
                    }
            return response_data
        except ValidationError as err:
            raise UseCaseException(loads(err.json()), error_code=error_status.VALIDATION_ERROR)
