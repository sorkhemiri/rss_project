from fastapi import APIRouter, Depends
from starlette.requests import Request

from usecase.feed.implementation import SubscribeRSSSourceUseCase

from entities import User
from utils.auth import check_authentication

router = APIRouter()


@router.get("/source/{source_id}/subscribe/", tags=["sources-list", "feed"])
def rss_sources_list(request: Request, source_id: int, user: User = Depends(check_authentication)):
    use_case = SubscribeRSSSourceUseCase()
    return use_case.execute(request_model={"source_id": source_id, "user": user})
