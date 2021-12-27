from typing import Type

from json import loads
from pydantic import ValidationError

from exceptions import error_status
from interfaces.validator import ValidatorInterface
from interfaces.use_case import UseCaseInterface
from interfaces.user_auth_repository_interface import UserAuthRepositoryInterface
from exceptions import UseCaseException


class LogoutUseCase(UseCaseInterface):
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
            if request_data.auth_token:
                uid = self.user_auth_repository.authenticated(access_token=request_data.auth_token)
                if uid:
                    uid = str(uid)
                    self.user_auth_repository.logout(uid=uid)
            response_data = {
                "result": "User logout successfully",
                "http_status_code": 200
            }
            return response_data
        except ValidationError as err:
            raise UseCaseException(loads(err.json()), error_code=error_status.VALIDATION_ERROR)
