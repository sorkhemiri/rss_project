from app import db

from repositories.postgres import RSSSourceRepository

RSSSourceRepository.create_rss_sources()