from fastapi import APIRouter
from api.api_v1.account import router as account_router


router = APIRouter()
router.include_router(account_router, prefix='/account')
