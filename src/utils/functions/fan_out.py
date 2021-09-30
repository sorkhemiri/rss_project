from datetime import datetime
from typing import List

from repositories.redis import FeedManager
from repositories.postgres.subscription import SubscriptionRepository


def fan_out(key: str, rss_ids: List[int]):
    now_time = datetime.now()
    data_values = []
    for post_id in rss_ids:
        post_serial_id = f"{int(now_time.timestamp())}{post_id}"
        data_values.append((post_id, post_serial_id))
    FeedManager.add_to_channel(key=key, feed=data_values)
    subscribers = SubscriptionRepository.get_channel_subscriber_by_key(key=key)
    for subscriber in subscribers:
        FeedManager.add_to_feed(user_id=subscriber.user.id, feed=data_values)
