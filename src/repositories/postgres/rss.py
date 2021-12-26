from typing import List

from pony import orm

from entities import RSS, RSSSource
from interfaces.rss_repository_interface import RSSRepositoryInterface
from models import RSS as RSSDB, RSSSource as RSSSourceDB
from exceptions import RepositoryException


class RSSRepository(RSSRepositoryInterface):

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

    @classmethod
    def get_list(cls, rss_ids: List[int]):
        with orm.db_session:
            rss_ids_str = str(rss_ids).replace("[", "(").replace("]", ")")

            rss_data = db.select("select id, title, link, description, source, pub_date from RSS "
                                  "where id in {} "
                                  "and (is_deleted is null or is_deleted = FALSE)".format(rss_ids_str))
            rss_list = [
                RSS(
                    id=item[0],
                    title=item[1],
                    link=item[2],
                    description=item[3],
                    source=RSSSource(id=item[4]),
                    pub_date=item[5]
                )
                for item in
                rss_data
            ]
            return rss_list
