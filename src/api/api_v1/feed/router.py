from fastapi import APIRouter
from api.api_v1.feed.endpoints.rss_sources_list import router as rss_sources_list_router
from api.api_v1.feed.endpoints.subscribe_rss_source import router as subscribe_rss_source_router
from api.api_v1.feed.endpoints.unsubscribe_rss_source import router as unsubscribe_rss_source_router


router = APIRouter()

router.include_router(rss_sources_list_router)
router.include_router(subscribe_rss_source_router)
router.include_router(unsubscribe_rss_source_router)
