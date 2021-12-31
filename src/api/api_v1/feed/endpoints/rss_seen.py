from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from entities import User
from pydantic import BaseModel
from repositories.postgres import UserRepository
from repositories.redis import UserAuthRepository, FeedManagerRepository
from usecase.feed.implementation import RemoveFromUnseenUseCase
from dependencies import CheckAuthentication
from validators.feed import RemoveFromUnseenValidator

router = APIRouter()

auth_check = CheckAuthentication(
    user_repository=UserRepository, user_auth_repository=UserAuthRepository
)


class RSSDataStruct(BaseModel):
    source_key: str
    rss_ids: List[int]


class RequestData(BaseModel):
    rss_data: List[RSSDataStruct]


@router.post("/user/seen/", tags=["user-likes", "feed"])
def user_seen(
    request: Request, request_data: RequestData, user: User = Depends(auth_check)
):
    request_data = request_data.dict()
    request_data.update({"user": user})
    use_case = RemoveFromUnseenUseCase(
        validator=RemoveFromUnseenValidator, feed_manager_repository=FeedManagerRepository
    )
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
