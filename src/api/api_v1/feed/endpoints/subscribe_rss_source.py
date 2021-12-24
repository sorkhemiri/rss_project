from fastapi import APIRouter, Depends
from starlette.requests import Request

from usecase.feed.implementation import SubscribeRSSSourceUseCase

from entities import User
from utils import check_authentication

router = APIRouter()


@router.post("/source/{source_id}/subscribe/", tags=["source-subscribe", "feed"])
def rss_source_subscribe(request: Request, source_id: int, user: User = Depends(check_authentication)):
    use_case = SubscribeRSSSourceUseCase()
    return use_case.execute(request_model={"source_id": source_id, "user": user})
