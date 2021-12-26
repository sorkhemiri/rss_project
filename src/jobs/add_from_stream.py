from datetime import datetime
import logging

import feedparser

from app import db
from entities import RSS
from repositories.postgres import RSSSourceRepository, RSSRepository
from repositories.redis import FeedMemory
from decorators import retry
from utils import fan_out
from celery_app import celery_app


@celery_app.task
@retry(times=3, wait=5)
def add_from_stream():
    sources = RSSSourceRepository.get_sources()
    for source in sources:
        feed = feedparser.parse(source.link)
        rss_ids = FeedMemory.get_memory(key=source.key, date=datetime.now())
        stored_rss_ids = []
        stored_post_ids = []
        for item in feed["entries"]:
            if source.key == "varzesh3":
                logging.info("source with key varzesh3 init")
                link = item.link
                link = link.replace("http://www.varzesh3.com/news/", "")
                rss_id = link.split("/")[0]
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
                stored_post_ids.append(created_rss.id)
                logging.info(f"rss_id --{rss_id}-- saved")
                stored_rss_ids.append(rss_id)
        fan_out(key=source.key, rss_ids=stored_post_ids)
        FeedMemory.add_to_memory(key=source.key, post_ids=stored_rss_ids, date=datetime.now())