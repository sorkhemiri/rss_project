from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from repositories.redis import UserAuthRepository
from usecase.account.implementation import RefreshAccessUseCase
from validators.account import RefreshAccessValidator

router = APIRouter()


class RequestData(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/refresh", tags=["refresh-access", "auth"])
def refresh_access(request: Request, request_data: RequestData):
    request_data = request_data.dict()
    use_case = RefreshAccessUseCase(
        validator=RefreshAccessValidator, user_auth_repository=UserAuthRepository
    )

    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
