from fastapi import APIRouter, Depends
from starlette.requests import Request

from entities import User
from usecase.feed.implementation import UnlikeRSSUseCase
from utils.auth import check_authentication

router = APIRouter()


@router.post("/rss/{rss_id}/unlike/", tags=["unlike-rss", "feed"])
def rss_list(request: Request, rss_id: int, user: User = Depends(check_authentication)):
    use_case = UnlikeRSSUseCase()
    return use_case.execute(request_model={"rss_id": rss_id, "user": user})
