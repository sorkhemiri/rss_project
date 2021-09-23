from entities import User


class UserRepository:

    @classmethod
    def check_username_unique(cls, username: str) -> bool:
        pass

    @classmethod
    def create(cls, model: User) -> User:
        pass
