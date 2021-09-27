from pony import orm

from entities import Subscription
from models import Subscription as SubscriptionDB, db
from utils.exceptions import RepositoryException


class SubscriptionRepository:
    @classmethod
    def create(cls, model: Subscription) -> Subscription:
        with orm.db_session:
            model_data = model.dict(exclude_defaults=True)
            subscription_db = SubscriptionDB(**model_data)
            orm.commit()
            return model
