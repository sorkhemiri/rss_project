from typing import List

from pony import orm
from pony.orm import raw_sql

from entities import Subscription, User
from models import Subscription as SubscriptionDB, db, RSSSource as RSSSourceDB, User as UserDB
from utils.exceptions import RepositoryException


class SubscriptionRepository:
    @classmethod
    def create(cls, model: Subscription) -> Subscription:
        with orm.db_session:
            model_data = {}
            if model.source and model.source.id:
                source = RSSSourceDB[model.source.id]
                model_data["source"] = source
            if model.user:
                user = UserDB[model.source.id]
                model_data["user"] = user
            subscription_db = SubscriptionDB(**model_data)
            orm.commit()
            return model

    @classmethod
    def get_channel_subscriber_by_key(cls, key) -> List[Subscription]:
        with orm.db_session:
            sub_data = db.select(
                "select user"
                " from Subscription as s"
                " left join RSSSource as rs on rs.id = s.source"
                " where rs.key = $key and (s.is_deleted is null or s.is_deleted = FALSE)")
            sub_entities = [
                Subscription(user=User(id=item)) for item in sub_data
            ]
            return sub_entities
