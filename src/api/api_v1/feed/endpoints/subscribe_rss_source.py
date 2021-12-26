from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from repositories.postgres import RSSSourceRepository, SubscriptionRepository, UserRepository
from repositories.redis import UserAuthRepository
from usecase.feed.implementation import SubscribeRSSSourceUseCase

from entities import User
from dependencies import CheckAuthentication
from validators.feed import SubscribeRSSSourceValidator

router = APIRouter()

auth_check = CheckAuthentication(user_repository=UserRepository, user_auth_repository=UserAuthRepository)


@router.post("/source/{source_key}/subscribe/", tags=["source-subscribe", "feed"])
def rss_source_subscribe(request: Request, source_key: str, user: User = Depends(auth_check)):
    request_data = {
        "source_key": source_key,
        "user": user,
    }
    use_case = SubscribeRSSSourceUseCase(validator=SubscribeRSSSourceValidator,
                                         rss_source_repository=RSSSourceRepository,
                                         subscription_repository=SubscriptionRepository)
    data = use_case.execute(request_model=request_data or {})
    status = data["http_status_code"]
    del data["http_status_code"]
    return JSONResponse(content=data, status_code=status)
