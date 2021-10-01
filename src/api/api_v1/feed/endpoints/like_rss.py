from fastapi import APIRouter, Depends
from starlette.requests import Request

from entities import User
from usecase.feed.implementation import RSSLikeUseCase
from utils.auth import check_authentication

router = APIRouter()


@router.get("/rss/{rss_id}/like/", tags=["like-rss", "feed"])
def rss_list(request: Request, rss_id: int, user: User = Depends(check_authentication)):
    use_case = RSSLikeUseCase()
    return use_case.execute(request_model={"rss_id": rss_id, "user": user})
