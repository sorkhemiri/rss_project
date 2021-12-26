from fastapi import APIRouter, Depends
from starlette.requests import Request

from entities import User
from repositories.postgres import UserRepository
from repositories.redis import UserAuthRepository
from usecase.feed.implementation import RSSListUseCase
from dependencies import CheckAuthentication

router = APIRouter()

auth_check = CheckAuthentication(user_repository=UserRepository, user_auth_repository=UserAuthRepository)


@router.get("/rss/", tags=["rss-list", "feed"])
def rss_list(request: Request, page: int = 1, limit: int = 10, user: User = Depends(auth_check)):
    use_case = RSSListUseCase()
    return use_case.execute(request_model={"page": page, "limit": limit, "user": user})