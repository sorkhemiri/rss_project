from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from dependencies import CheckAdminStatus
from entities import User
from repositories.postgres import RSSSourceRepository, UserRepository
from repositories.redis import UserAuthRepository
from usecase.feed.implementation import DeleteRSSSourceUseCase
from validators.feed import DeleteRSSSourceValidator

router = APIRouter()


class RequestData(BaseModel):
    key: str


auth_check = CheckAdminStatus(user_repository=UserRepository, user_auth_repository=UserAuthRepository)


@router.delete("/source/delete/", tags=["delete-source", "feed"])
def delete_rss_source(request: Request, request_data: RequestData, user: User = Depends(auth_check)):
    request_data = request_data.dict()
    use_case = DeleteRSSSourceUseCase(validator=DeleteRSSSourceValidator,
                                      rss_source_repository=RSSSourceRepository)
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
