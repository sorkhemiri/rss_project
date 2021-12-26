from fastapi import APIRouter, Depends
from starlette.requests import Request

from entities import User
from repositories.postgres import UserRepository
from repositories.redis import UserAuthRepository
from usecase.feed.implementation import LikeRSSUseCase
from dependencies import CheckAuthentication

router = APIRouter()

auth_check = CheckAuthentication(user_repository=UserRepository, user_auth_repository=UserAuthRepository)


@router.post("/rss/{rss_id}/like/", tags=["like-rss", "feed"])
def rss_list(request: Request, rss_id: int, user: User = Depends(auth_check)):
    use_case = LikeRSSUseCase()
    return use_case.execute(request_model={"rss_id": rss_id, "user": user})
