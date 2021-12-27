from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from entities import User
from repositories.postgres import UserRepository, LikeRepository
from repositories.redis import UserAuthRepository
from usecase.feed.implementation import UnlikeRSSUseCase
from dependencies import CheckAuthentication
from validators.feed import SubscribeRSSSourceValidator

router = APIRouter()

auth_check = CheckAuthentication(user_repository=UserRepository, user_auth_repository=UserAuthRepository)


@router.post("/rss/{rss_id}/unlike/", tags=["unlike-rss", "feed"])
def rss_unlike(request: Request, rss_id: int, user: User = Depends(auth_check)):
    request_data = {
        "rss_id": rss_id,
        "user": user
    }
    use_case = UnlikeRSSUseCase(validator=SubscribeRSSSourceValidator,
                                like_repository=LikeRepository)
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
