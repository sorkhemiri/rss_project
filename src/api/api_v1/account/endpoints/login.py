from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from usecase.account.implementation import LoginUseCase

router = APIRouter()


class RequestData(BaseModel):
    username: str
    password: str


@router.post("/login", tags=["user_login", "auth"])
def login(request: Request, request_data: RequestData):
    data = request_data.dict()
    use_case = LoginUseCase()
    return use_case.execute(request_model=data)
