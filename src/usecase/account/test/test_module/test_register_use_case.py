
from repositories.postgres import UserRepository
from usecase.account.implementation import RegisterUseCase
from validators.account import RegisterValidator


class RegisterUseCaseTestCase:
    @staticmethod
    def test_input():

        use_case = RegisterUseCase(
            validator=RegisterValidator, user_repository=UserRepository
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
    def test_username_already_exist(username_present_patch):
        use_case = RegisterUseCase(
            validator=RegisterValidator, user_repository=UserRepository
        )

        request_data = {"username": "JohnDoe", "password": "VeryStrongPass"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
        assert data["message"] == "username already exists"

    @staticmethod
    def test_username_not_valid(username_absent_patch):
        use_case = RegisterUseCase(
            validator=RegisterValidator, user_repository=UserRepository
        )

        request_data = {"username": "not*valid$username", "password": "VeryStrongPass"}
        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
        assert data["message"] == "username not valid"

    @staticmethod
    def test_short_password(username_absent_patch, pattern_match_patch):
        use_case = RegisterUseCase(
            validator=RegisterValidator, user_repository=UserRepository
        )

        request_data = {"username": "JohnDoe", "password": "Pass"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
        assert data["message"] == "password too short"

    @staticmethod
    def test_outcome(username_absent_patch, create_user_patch):

        use_case = RegisterUseCase(
            validator=RegisterValidator, user_repository=UserRepository
        )

        request_data = {"username": "JohnDoe", "password": "VeryStrongPass"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["user"] == {
                                    "uid": "bd9213db-8d4c-4da4-9c77-e8e92172fa88",
                                    "username": "johndoe"
                                }

        request_data = {"username": "JohnDoe", "password": "VeryStrongPass", "first_name": "John"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["user"] == {
            "uid": "bd9213db-8d4c-4da4-9c77-e8e92172fa88",
            "username": "johndoe",
            "first_name": "John",
        }

        request_data = {"username": "JohnDoe", "password": "VeryStrongPass", "first_name": "John", "last_name": "Doe"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["user"] == {
            "uid": "bd9213db-8d4c-4da4-9c77-e8e92172fa88",
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe"
        }
