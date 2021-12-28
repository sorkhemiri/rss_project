from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from repositories.postgres import UserRepository
from repositories.redis import UserAuthRepository
from usecase.account.implementation import LoginUseCase
from validators.account import LoginValidator

router = APIRouter()


class RequestData(BaseModel):
    username: str
    password: str


@router.post("/login", tags=["user_login", "auth"])
def login(request: Request, request_data: RequestData):
    request_data = request_data.dict()
    use_case = LoginUseCase(
        validator=LoginValidator,
        user_auth_repository=UserAuthRepository,
        user_repository=UserRepository,
    )

    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
