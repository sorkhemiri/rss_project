from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from entities import User
from repositories.postgres import UserRepository, LikeRepository, RSSSourceRepository
from repositories.redis import UserAuthRepository
from usecase.feed.implementation import UserSourceLikesListUseCase
from dependencies import CheckAuthentication
from validators.feed import UserSourceLikesListValidator

router = APIRouter()

auth_check = CheckAuthentication(
    user_repository=UserRepository, user_auth_repository=UserAuthRepository
)


@router.get("/user/{source_key}/likes/", tags=["user-source-likes", "feed"])
def user_source_likes(
    request: Request,
    source_key: str,
    offset: int = 0,
    limit: int = 10,
    user: User = Depends(auth_check),
):
    request_data = {
        "offset": offset,
        "limit": limit,
        "user": user,
        "source_key": source_key,
    }
    use_case = UserSourceLikesListUseCase(
        validator=UserSourceLikesListValidator,
        like_repository=LikeRepository,
        rss_source_repository=RSSSourceRepository,
    )
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
