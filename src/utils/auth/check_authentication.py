from typing import Optional

from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from entities import User
from repositories.postgres import UserRepository
from repositories.redis import UserAuthenticate


def check_authentication(request: Request) -> Optional[User]:
    auth_bearer_token = request.headers.get("Authorization")
    if auth_bearer_token:
        auth_token = auth_bearer_token.replace("Bearer ", "")
        user_id = UserAuthenticate.is_authenticated(token=auth_token)
        if user_id:
            if not UserRepository.check_user_exist(user_id=user_id):
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
