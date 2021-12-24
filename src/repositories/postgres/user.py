from pony import orm

from entities import User
from interfaces.user_repository_interface import UserRepositoryInterface
from models import User as UserDB, db
from utils import make_password
from exceptions import RepositoryException


class UserRepository(UserRepositoryInterface):

    @classmethod
    def check_username_exist(cls, username: str) -> bool:
        with orm.db_session:
            if db.exists("""select id from User 
            where username = $username and (is_deleted is null or is_deleted = FALSE)"""):
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
            passwords = db.select("select password from User "
                                  "where username = $username "
                                  "and (is_deleted is null or is_deleted = FALSE) limit 1")
            if not passwords:
                raise RepositoryException(message="user password not set")
            db_password = passwords[0]
            if password_hash == db_password:
                return True
        return False

    @classmethod
    def get_user_id_by_username(cls, username: str) -> int:
        with orm.db_session:
            ids = db.select("select id from User "
                            "where username = $username "
                            "and (is_deleted is null or is_deleted = FALSE) limit 1")
            if not ids:
                raise RepositoryException(message="user not found")
            user_id = ids[0]
            return user_id

    @classmethod
    def check_user_exist(cls, user_id: int) -> bool:
        with orm.db_session:
            if db.exists("select id from User "
                         "where id = $user_id "
                         "and (is_deleted is null or is_deleted = FALSE)"):
                return True
            return False
