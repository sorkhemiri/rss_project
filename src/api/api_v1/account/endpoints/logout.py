from typing import Optional

from fastapi import APIRouter, Header
from starlette.requests import Request
from starlette.responses import JSONResponse

from repositories.redis import UserAuthRepository
from usecase.account.implementation import LogoutUseCase
from validators.account import LogoutValidator

router = APIRouter()


@router.post("/logout", tags=["user_logout", "auth"])
def logout(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.replace("Bearer ", "")
        request_data = {"auth_token": auth_token}
    else:
        request_data = None
    use_case = LogoutUseCase(
        validator=LogoutValidator, user_auth_repository=UserAuthRepository
    )

    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
