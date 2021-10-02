from uuid import uuid4

import json
import jwt
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from repositories.postgres import UserRepository
from repositories.redis import UserAuthenticate
from settings import env_config
from usecase.interface import UseCaseInterface

from utils.exceptions import UseCaseException, status
from validators.account import LoginValidator


class LoginUseCase(UseCaseInterface):
    def process_request(self, request_dict: dict):
        try:
            data = LoginValidator(**request_dict)
            if not UserRepository.check_username_exist(username=data.username):
                raise UseCaseException(message="user not found", error_code=status.DOES_NOT_EXIST_ERROR)
            if not UserRepository.check_password(username=data.username, password=data.password):
                raise UseCaseException(message="password incorrect", error_code=status.DOES_NOT_EXIST_ERROR)
            user_id = UserRepository.get_user_id_by_username(username=data.username)
            unique_token = str(uuid4())
            token = jwt.encode(
                {"user_id": user_id, "unique_token": unique_token},
                env_config.SECRET_KEY,
                algorithm="HS256",
            )
            UserAuthenticate.login(user_id, token)
            return JSONResponse(content={"token": token}, status_code=HTTP_200_OK)
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
