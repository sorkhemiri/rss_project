from fastapi import APIRouter
from api.api_v1.feed.endpoints.rss_sources_list import router as rss_sources_list_router


router = APIRouter()

router.include_router(rss_sources_list_router)
