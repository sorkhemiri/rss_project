from repositories.redis import UserAuthRepository
from usecase.account.implementation import LogoutUseCase
from validators.account import LogoutValidator


class LogoutUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = LogoutUseCase(
            validator=LogoutValidator, user_auth_repository=UserAuthRepository
        )

        request_data = {}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_logout_valid_token(access_token_valid_patch, logout_patch):
        use_case = LogoutUseCase(
            validator=LogoutValidator, user_auth_repository=UserAuthRepository
        )

        request_data = {"auth_token": "fake_auth_token"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == "User logout successfully"

    @staticmethod
    def test_logout_invalid_token(access_token_not_valid_patch, logout_patch):
        use_case = LogoutUseCase(
            validator=LogoutValidator, user_auth_repository=UserAuthRepository
        )

        request_data = {"auth_token": "fake_auth_token"}

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == "User logout successfully"
