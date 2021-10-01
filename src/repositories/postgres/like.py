from pony import orm

from entities import Like
from models import db, User as UserDB, RSS as RSSDB, Like as LikeDB
from utils.exceptions import RepositoryException, status


class LikeRepository:
    @classmethod
    def user_like_exist(cls, model: Like) -> bool:
        if not model.user and not model.user.id:
            raise RepositoryException(message="user id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
        if not model.rss and not model.rss.id:
            RepositoryException(message="rss id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
        like_data = db.select("select id from Like "
                             "where rss=$model.rss.id and user=$model.user.id"
                             "and (is_deleted is null or is_deleted = FALSE)")
        if like_data:
            return True
        return False

    @classmethod
    def create(cls, model: Like) -> Like:
        with orm.db_session:
            model_data = {}
            if model.rss and model.rss.id:
                rss = RSSDB[model.rss.id]
                model_data["rss"] = rss
            if model.user:
                user = UserDB[model.user.id]
                model_data["user"] = user
            like_db = LikeDB(**model_data)
            orm.commit()
            model.id = like_db.id
            return model
