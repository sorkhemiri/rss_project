from app import db
from entities import RSSSource

from repositories.postgres import RSSSourceRepository
rss_source_data = [
            {
                "title": "ورزش سه | آخرین اخبار",
                "link": "http://varzesh3.com/rss/all",
                "key": "varzesh3",
                "description": "آخرين اخبار ورزشی",
            }
        ]
source_entities = [RSSSource(**item) for item in rss_source_data]
for source in source_entities:
    if not RSSSourceRepository.check_source_key_exists(key=source.key):
        RSSSourceRepository.create(model=source)
