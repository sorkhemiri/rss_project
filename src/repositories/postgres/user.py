from pony import orm

from entities import User
from models import User as UserDB, db
from utils.functions import make_password


class UserRepository:

    @classmethod
    def check_username_exist(cls, username: str) -> bool:
        with orm.db_session:
            if db.exists("select id from User where username = $username"):
                return True
            return False

    @classmethod
    def create(cls, model: User) -> User:
        model.password = make_password(password=model.password)
        with orm.db_session:
            model_data = model.dict(exclude_defaults=True)
            user_db = UserDB(**model_data)
            orm.commit()
            model.password = None
            model.id = user_db.id
            return model

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        password_hash = make_password(password=password)
        with orm.db_session:
            users = db.select("select username from User where username = $username limit 1")
            user = users[0]
            if password_hash == user.password:
                return True
        return False


    @classmethod
    def get_user_id_by_username(cls, username: str) -> int:
        pass

    @classmethod
    def check_user_exist(cls, user_id: int) -> bool:
        pass
