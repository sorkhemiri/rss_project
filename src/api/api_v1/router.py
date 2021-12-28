from fastapi import APIRouter
from api.api_v1.account import router as account_router
from api.api_v1.feed import router as feed_router


router = APIRouter()
router.include_router(account_router, prefix="/account")
router.include_router(feed_router, prefix="/feed")
