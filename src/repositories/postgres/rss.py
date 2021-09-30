from pony import orm

from entities import RSS
from models import RSS as RSSDB, RSSSource as RSSSourceDB


class RSSRepository:

    @classmethod
    def create(cls, model: RSS) -> RSS:
        with orm.db_session:
            model_data = model.dict(exclude_defaults=True)
            if model.source and model.source.id:
                model_data["source"] = RSSSourceDB[model.source.id]
            rss_db = RSSDB(**model_data)
            orm.commit()
            model.id = rss_db.id
            return model
