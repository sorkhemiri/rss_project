from fastapi import APIRouter, Depends
from starlette.requests import Request

from entities import User
from usecase.feed.implementation import RSSListUseCase
from utils import check_authentication

router = APIRouter()


@router.get("/rss/", tags=["rss-list", "feed"])
def rss_list(request: Request, page: int = 1, limit: int = 10, user: User = Depends(check_authentication)):
    use_case = RSSListUseCase()
    return use_case.execute(request_model={"page": page, "limit": limit, "user": user})