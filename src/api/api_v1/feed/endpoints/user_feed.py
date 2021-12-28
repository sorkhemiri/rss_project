from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from entities import User
from repositories.postgres import UserRepository, RSSRepository
from repositories.redis import UserAuthRepository, FeedManagerRepository
from usecase.feed.implementation import UserFeedUseCase
from dependencies import CheckAuthentication
from validators.feed import RSSListValidator

router = APIRouter()

auth_check = CheckAuthentication(
    user_repository=UserRepository, user_auth_repository=UserAuthRepository
)


@router.get("/user/feed/", tags=["user-feed", "feed"])
def user_feed(
    request: Request, offset: int = 0, limit: int = 10, user: User = Depends(auth_check)
):
    request_data = {"offset": offset, "limit": limit, "user": user}
    use_case = UserFeedUseCase(
        validator=RSSListValidator,
        rss_repository=RSSRepository,
        feed_manager_repository=FeedManagerRepository,
    )
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
