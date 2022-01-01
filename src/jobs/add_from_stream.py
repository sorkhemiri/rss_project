import logging
import re
import time
from multiprocessing.pool import ThreadPool

import feedparser

from entities import RSS
from interfaces.feed_manager_repository_interface import FeedManagerRepositoryInterface
from repositories.postgres import RSSSourceRepository, RSSRepository
from repositories.redis import FeedMemoryRepository, FeedManagerRepository
from decorators import retry
from celery_app import celery_app

from datetime import datetime
from typing import List, Type

from repositories.postgres.subscription import SubscriptionRepository
from settings import env_config
from settings.constants import JOB_CONCURRENCY, SOURCES_CHUNK_LIMIT


def fan_out(
    key: str,
    rss_ids: List[int],
    feed_manager_repository: Type[FeedManagerRepositoryInterface],
):
    now_time = datetime.now()
    data_values = []
    for post_id in rss_ids:
        post_serial_id = f"{int(now_time.timestamp())}{post_id}"
        data_values.append((post_id, post_serial_id))
    feed_manager_repository.add_to_channel(key=key, feed=data_values)
    subscribers = SubscriptionRepository.get_channel_subscriber_by_key(key=key)
    for subscriber in subscribers:
        feed_manager_repository.add_to_feed(
            user_id=subscriber.user.id, feed=data_values
        )
        feed_manager_repository.add_to_unseen(
            user_id=subscriber.user.id, post_ids=rss_ids
        )
        feed_manager_repository.add_to_source_unseen(
            user_id=subscriber.user.id, source_key=key, post_ids=rss_ids
        )


def inner_function(source):
    retry_nums = 0
    while True:
        try:
            feed = feedparser.parse(source.link)
            rss_ids = FeedMemoryRepository.get_memory(key=source.key, date=datetime.now())
            stored_rss_ids = []
            stored_db_ids = []
            for item in feed["entries"]:
                logging.info(f"source with key {source.key} init")
                link = item.link
                rss_id_patterns = re.findall(pattern="/[0-9]+/", string=link)
                rss_id = rss_id_patterns.pop().replace("/", "") if rss_id_patterns else None
                logging.info(f"rss_id --{rss_id}-- got in stream")
                if rss_id in rss_ids:
                    logging.info(f"rss_id --{rss_id}-- abort")
                    continue
                rss = RSS()
                rss.link = item.link
                rss.title = item.title
                rss.source = source
                rss.description = item.summary
                pub_date_str = item.published
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%dT%H:%M:%S")
                rss.pub_date = pub_date
                created_rss = RSSRepository.create(model=rss)
                stored_db_ids.append(created_rss.id)
                logging.info(f"rss_id --{rss_id}-- saved")
                stored_rss_ids.append(rss_id)
            fan_out(
                key=source.key,
                rss_ids=stored_db_ids,
                feed_manager_repository=FeedManagerRepository,
            )
            FeedMemoryRepository.add_to_memory(
                key=source.key, post_ids=stored_rss_ids, date=datetime.now()
            )
        except Exception as ex:
            if retry_nums > env_config.retry_count:
                RSSSourceRepository.make_update_need(source_key=source.key)
            else:
                retry_nums += 1
                time.sleep(env_config.retry_duration)


@celery_app.task
def add_from_stream():
    chunks = []
    last_offset = 0
    while True:
        sources = RSSSourceRepository.get_sources(
            limit=SOURCES_CHUNK_LIMIT, offset=last_offset
        )
        last_offset += SOURCES_CHUNK_LIMIT
        if sources:
            chunks.append(sources)
        else:
            break

    for chunk in chunks:
        with ThreadPool(processes=JOB_CONCURRENCY) as thread_pool:
            result = thread_pool.map_async(inner_function, chunk)
            result.get()


# add_from_stream()
