from entities import User


class UserRepository:

    @classmethod
    def check_username_exist(cls, username: str) -> bool:
        pass

    @classmethod
    def create(cls, model: User) -> User:
        pass

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        pass

    @classmethod
    def get_user_id_by_username(cls, username: str) -> int:
        pass
