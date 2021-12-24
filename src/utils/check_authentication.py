from typing import Optional, Type

from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from entities import User
from interfaces.user_auth_repository_interface import UserAuthRepositoryInterface
from interfaces.user_repository_interface import UserRepositoryInterface


def check_authentication(request: Request,
                         user_repository: Type[UserRepositoryInterface],
                         user_auth_repository: Type[UserAuthRepositoryInterface]) -> Optional[User]:
    auth_bearer_token = request.headers.get("Authorization")
    if auth_bearer_token:
        auth_token = auth_bearer_token.replace("Bearer ", "")
        user_id = user_auth_repository.authenticated(access_token=auth_token)
        if user_id:
            if not user_repository.check_user_exist(user_id=user_id):
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="User Data Not Valid")
            user = User(id=user_id)
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authorization Token Not Valid")
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authorization Token Not Found")
    return user
