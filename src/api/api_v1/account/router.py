from fastapi import APIRouter
from api.api_v1.account.endpoints.login import router as login_router


router = APIRouter()
router.include_router(login_router)
