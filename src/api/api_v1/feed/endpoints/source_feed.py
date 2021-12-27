from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from dependencies import CheckAdminStatus
from entities import User
from repositories.postgres import RSSSourceRepository, UserRepository, RSSRepository
from repositories.redis import UserAuthRepository, FeedManagerRepository
from usecase.feed.implementation import GetRSSSourceFeedUseCase
from validators.feed import CreateRSSSourceValidator, GetRSSSourceFeedValidator

router = APIRouter()


@router.get("/source/{source_key}/feed/", tags=["source-feed", "feed"])
def create_rss_source(request: Request, source_key: str, page: int = 1, limit: int = 10):
    request_data = {
        "source_key": source_key,
        "page": page,
        "limit": limit,
    }
    use_case = GetRSSSourceFeedUseCase(validator=GetRSSSourceFeedValidator,
                                       rss_repository=RSSRepository,
                                       feed_manager_repository=FeedManagerRepository)
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
