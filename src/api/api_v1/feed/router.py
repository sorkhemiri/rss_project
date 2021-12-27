from fastapi import APIRouter
from api.api_v1.feed.endpoints.rss_sources_list import router as rss_sources_list_router
from api.api_v1.feed.endpoints.subscribe_rss_source import router as subscribe_rss_source_router
from api.api_v1.feed.endpoints.unsubscribe_rss_source import router as unsubscribe_rss_source_router
from api.api_v1.feed.endpoints.user_feed import router as user_feed_router
from api.api_v1.feed.endpoints.like_rss import router as like_rss_router
from api.api_v1.feed.endpoints.unlike_rss import router as unlike_rss_router
from api.api_v1.feed.endpoints.create_rss_source import router as create_rss_source_router
from api.api_v1.feed.endpoints.delete_rss_source import router as delete_rss_source_router
from api.api_v1.feed.endpoints.source_feed import router as source_feed_router
from api.api_v1.feed.endpoints.user_subscriptions import router as user_subscriptions_router
from api.api_v1.feed.endpoints.all_user_likes import router as all_user_likes_router


router = APIRouter()

router.include_router(create_rss_source_router)
router.include_router(delete_rss_source_router)
router.include_router(rss_sources_list_router)
router.include_router(subscribe_rss_source_router)
router.include_router(unsubscribe_rss_source_router)
router.include_router(user_feed_router)
router.include_router(like_rss_router)
router.include_router(unlike_rss_router)
router.include_router(source_feed_router)
router.include_router(user_subscriptions_router)
router.include_router(all_user_likes_router)
