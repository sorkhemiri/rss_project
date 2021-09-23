from re import fullmatch

import orjson as json
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from entities import User
from repositories.postgres import UserRepository
from usecase.interface import UseCaseInterface

from utils.exceptions import UseCaseException, status
from validators.account import RegisterValidator


class RegisterUseCase(UseCaseInterface):
    def process_request(self, request_dict: dict):
        try:
            data = RegisterValidator(**request_dict)
            if not UserRepository.check_username_unique(username=data.username):
                raise UseCaseException(message="username already exists", error_code=status.VALIDATION_ERROR)
            if not fullmatch(pattern="[a-zA-Z0-9_]{4}", string=data.username):
                raise UseCaseException(message="username not valid", error_code=status.VALIDATION_ERROR)
            user = User()
            user.user_name = data.username
            user.first_name = data.first_name
            user.last_name = data.last_name
            user.password = data.password
            created_user = UserRepository.create(model=user)
            user.password = None
            user.id = created_user.id
            return JSONResponse(content={"user": user.dict(exclude_defaults=True)}, status_code=HTTP_200_OK)
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
