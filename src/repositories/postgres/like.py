from pony import orm

from entities import Like
from models import db, User as UserDB, RSS as RSSDB, Like as LikeDB
from exceptions import RepositoryException, error_status


class LikeRepository:
    @classmethod
    def user_like_exist(cls, model: Like) -> bool:
        if not model.user and not model.user.id:
            raise RepositoryException(message="user id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
        if not model.rss and not model.rss.id:
            RepositoryException(message="rss id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
        with orm.db_session:
            like_data = db.select("select id from Like "
                                 "where rss=$model.rss.id and user=$model.user.id "
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

    @classmethod
    def delete(cls, model: Like):
        if not model.user and not model.user.id:
            raise RepositoryException(message="user id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
        if not model.rss and not model.rss.id:
            RepositoryException(message="rss id must be provided", error_code=status.DOES_NOT_EXIST_ERROR)
        rss_id = model.rss.id
        user_id = model.user.id
        with orm.db_session:
            like_data = db.select("select id from Like "
                                 "where rss = $rss_id and user = $user_id"
                                 " and (is_deleted is null or is_deleted = FALSE)")
            if like_data:
                like_id = like_data[0]
                LikeDB[like_id].set(is_deleted=True)
