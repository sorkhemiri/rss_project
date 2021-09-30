from datetime import datetime
from typing import List

from repositories.redis import FeedManager
from repositories.postgres.subscription import SubscriptionRepository


def fan_out(key: str, rss_ids: List[int]):
    now_time = datetime.now()
    FeedManager.add_to_channel(key=key, post_ids=rss_ids, date=now_time)
    subscribers = SubscriptionRepository.get_channel_subscriber_by_key(key=key)
    for subscriber in subscribers:
        FeedManager.add_to_feed(user_id=subscriber.user.id, post_ids=rss_ids, date=now_time)
