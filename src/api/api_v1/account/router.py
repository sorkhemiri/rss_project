from fastapi import APIRouter
from api.api_v1.account.endpoints.login import router as login_router
from api.api_v1.account.endpoints.register import router as register_router
from api.api_v1.account.endpoints.refresh_access import router as refresh_access_router
from api.api_v1.account.endpoints.logout import router as logout_router


router = APIRouter()
router.include_router(login_router)
router.include_router(register_router)
router.include_router(refresh_access_router)
router.include_router(logout_router)
