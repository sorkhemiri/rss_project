from typing import Optional, Type

from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from entities import User
from interfaces.user_auth_repository_interface import UserAuthRepositoryInterface
from interfaces.user_repository_interface import UserRepositoryInterface


class CheckAuthentication:
    def __init__(
            self,
            user_repository: Type[UserRepositoryInterface],
            user_auth_repository: Type[UserAuthRepositoryInterface]
    ):
        self.user_repository = user_repository
        self.user_auth_repository = user_auth_repository

    def __call__(self, request: Request):
        auth_bearer_token = request.headers.get("Authorization")
        if auth_bearer_token:
            auth_token = auth_bearer_token.replace("Bearer ", "")
            uid = self.user_auth_repository.authenticated(access_token=auth_token)
            if uid:
                if not self.user_repository.check_user_exist(uid=uid):
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="User Data Not Valid")
                user_id = self.user_repository.get_user_id_by_uid(uid=uid)
                user = User(id=user_id, uid=uid)
            else:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Authorization Token Not Valid")
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authorization Token Not Found")
        return user
