from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from repositories.postgres import UserRepository
from usecase.account.implementation import RegisterUseCase
from validators.account import RegisterValidator

router = APIRouter()


class RequestData(BaseModel):
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@router.post("/register", tags=["user_register", "auth"])
def register(request: Request, request_data: RequestData):
    request_data = request_data.dict()
    use_case = RegisterUseCase(validator=RegisterValidator,
                               user_repository=UserRepository)
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
