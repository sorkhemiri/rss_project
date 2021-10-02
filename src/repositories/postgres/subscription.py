from typing import List

from pony import orm
from pony.orm import raw_sql

from entities import Subscription, User
from models import Subscription as SubscriptionDB, db, RSSSource as RSSSourceDB, User as UserDB
from utils.exceptions import RepositoryException, status


class SubscriptionRepository:
    @classmethod
    def create(cls, model: Subscription) -> Subscription:
        with orm.db_session:
            model_data = {}
            if model.source and model.source.id:
                source = RSSSourceDB[model.source.id]
                model_data["source"] = source
            if model.user:
                user = UserDB[model.user.id]
                model_data["user"] = user
            subscription_db = SubscriptionDB(**model_data)
            orm.commit()
            model.id = subscription_db.id
            return model

    @classmethod
    def delete(cls, model: Subscription):
        with orm.db_session:
            if not model.user or not model.user.id:
                raise RepositoryException(message="user id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
            if not model.user or not model.user.id:
                raise RepositoryException(message="source id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
            source_id = model.source.id
            user_id = model.user.id
            sub_data = db.select("select id from Subscription "
                      "where source = $source_id and user = $user_id"
                      " and (is_deleted is null or is_deleted = FALSE)")
            if sub_data:
                sub_id = sub_data[0]
                SubscriptionDB[sub_id].set(is_deleted=True)

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

    @classmethod
    def check_subscription_exist(cls, model: Subscription) -> bool:
        with orm.db_session:
            if not model.user or not model.user.id:
                raise RepositoryException(message="user id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
            if not model.user or not model.user.id:
                raise RepositoryException(message="source id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
            sub_data = db.select("select id from Subscription "
                      "where source=$model.source.id and user=$model.user.id "
                      "and (is_deleted is null or is_deleted = FALSE)")
            if sub_data:
                return True
            return False
