from fastapi import APIRouter, Depends
from starlette.requests import Request

from repositories.postgres import UserRepository
from repositories.redis import UserAuthRepository
from usecase.feed.implementation import UnsubscribeRSSSourceUseCase

from entities import User
from dependencies import CheckAuthentication

router = APIRouter()

auth_check = CheckAuthentication(user_repository=UserRepository, user_auth_repository=UserAuthRepository)


@router.post("/source/{source_id}/unsubscribe/", tags=["source-unsubscribe", "feed"])
def rss_source_unsubscribe(request: Request, source_id: int, user: User = Depends(auth_check)):
    use_case = UnsubscribeRSSSourceUseCase()
    return use_case.execute(request_model={"source_id": source_id, "user": user})
