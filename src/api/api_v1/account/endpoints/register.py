from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from usecase.account.implementation import RegisterUseCase

router = APIRouter()


class RequestData(BaseModel):
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@router.post("/register", tags=["user_register", "auth"])
def register(request: Request, request_data: RequestData):
    data = request_data.dict()
    use_case = RegisterUseCase()
    return use_case.execute(request_model=data)
