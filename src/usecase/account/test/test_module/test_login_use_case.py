from repositories.postgres import UserRepository
from repositories.redis import UserAuthRepository
from usecase.account.implementation import LoginUseCase
from validators.account import LoginValidator


class LoginUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = LoginUseCase(
            validator=LoginValidator,
            user_auth_repository=UserAuthRepository,
            user_repository=UserRepository,
        )

        request_data = {"username": "JohnDoe"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {"password": "VeryStrongPass"}
        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_username_already_exist(username_absent_patch):
        use_case = LoginUseCase(
            validator=LoginValidator,
            user_auth_repository=UserAuthRepository,
            user_repository=UserRepository,
        )

        request_data = {"username": "JohnDoe", "password": "VeryStrongPass"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 404
        assert data["type"] == "DOES NOT EXIST ERROR"
        assert data["message"] == "User not found"

    @staticmethod
    def test_incorrect_password(username_present_patch, password_incorrect_patch):
        use_case = LoginUseCase(
            validator=LoginValidator,
            user_auth_repository=UserAuthRepository,
            user_repository=UserRepository,
        )

        request_data = {"username": "JohnDoe", "password": "VeryStrongPass"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
        assert data["message"] == "Password incorrect"

    @staticmethod
    def test_outcome(
        username_present_patch,
        password_correct_patch,
        uid_by_username_patch,
        login_patch,
    ):
        use_case = LoginUseCase(
            validator=LoginValidator,
            user_auth_repository=UserAuthRepository,
            user_repository=UserRepository,
        )

        request_data = {"username": "JohnDoe", "password": "VeryStrongPass"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == {
            "result": {
                "access": {
                    "token": "cca4eb1fa7a244d42895e1f1dd7f89253928b0e65db7d99e692e8f253778c3af",
                    "expire": "2021-12-29T10:24:35",
                },
                "refresh": {
                    "token": "f2301ecdc55a568264d9d7b32c0f1cf36719d1c72a409e1488090bd9fae6b180",
                    "expire": "2021-12-29T18:14:35",
                },
            }
        }
