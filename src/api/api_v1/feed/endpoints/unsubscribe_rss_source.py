from fastapi import APIRouter, Depends
from starlette.requests import Request

from usecase.feed.implementation import UnsubscribeRSSSourceUseCase

from entities import User
from utils.auth import check_authentication

router = APIRouter()


@router.post("/source/{source_id}/unsubscribe/", tags=["source-unsubscribe", "feed"])
def rss_source_unsubscribe(request: Request, source_id: int, user: User = Depends(check_authentication)):
    use_case = UnsubscribeRSSSourceUseCase()
    return use_case.execute(request_model={"source_id": source_id, "user": user})
