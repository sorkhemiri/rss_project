from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from dependencies import CheckAuthentication
from entities import User
from repositories.postgres import RSSRepository, UserRepository
from repositories.redis import FeedManagerRepository, UserAuthRepository
from usecase.feed.implementation import GetRSSSourceFeedUseCase
from validators.feed import GetRSSSourceFeedValidator

router = APIRouter()

auth_check = CheckAuthentication(
    user_repository=UserRepository, user_auth_repository=UserAuthRepository
)


@router.get("/source/{source_key}/feed/", tags=["source-feed", "feed"])
def source_feed(request: Request, source_key: str, page: int = 1, limit: int = 10, user: User = Depends(auth_check)):
    request_data = {
        "source_key": source_key,
        "page": page,
        "limit": limit,
        "user": user,
    }
    use_case = GetRSSSourceFeedUseCase(
        validator=GetRSSSourceFeedValidator,
        rss_repository=RSSRepository,
        feed_manager_repository=FeedManagerRepository,
    )
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
