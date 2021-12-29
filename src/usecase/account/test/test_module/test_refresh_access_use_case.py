from repositories.redis import UserAuthRepository
from usecase.account.implementation import RefreshAccessUseCase
from validators.account import RefreshAccessValidator


class RefreshAccessUseCaseTestCase:
    @staticmethod
    def test_input():
        use_case = RefreshAccessUseCase(
                                        validator=RefreshAccessValidator,
                                        user_auth_repository=UserAuthRepository
        )

        request_data = {
                    "access_token": "fake_access_token"
                }

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

        request_data = {
            "refresh_token": "fake_refresh_token"
        }
        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"

    @staticmethod
    def test_invalid_refresh_token(access_token_not_valid_patch, refresh_token_not_valid_patch):
        use_case = RefreshAccessUseCase(
            validator=RefreshAccessValidator,
            user_auth_repository=UserAuthRepository
        )

        request_data = {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token"
        }

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 400
        assert data["type"] == "VALIDATION ERROR"
        assert data["message"] == "refresh token invalid or expired"

    @staticmethod
    def test_use_of_access_token(access_token_valid_patch, get_auth_data_patch):
        use_case = RefreshAccessUseCase(
            validator=RefreshAccessValidator,
            user_auth_repository=UserAuthRepository
        )

        request_data = {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token"
        }

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == {
                                    "result": {
                                        "access": {
                                            "token": "cca4eb1fa7a244d42895e1f1dd7f89253928b0e65db7d99e692e8f253778c3af",
                                            "expire": "2021-12-29T10:24:35"
                                        },
                                        "refresh": {
                                            "token": "f2301ecdc55a568264d9d7b32c0f1cf36719d1c72a409e1488090bd9fae6b180",
                                            "expire": "2021-12-29T18:14:35"
                                        }
                                    }
                                }

    @staticmethod
    def test_use_of_refresh_token(access_token_not_valid_patch, refresh_token_valid_patch):
        use_case = RefreshAccessUseCase(
            validator=RefreshAccessValidator,
            user_auth_repository=UserAuthRepository
        )

        request_data = {
            "access_token": "fake_access_token",
            "refresh_token": "fake_refresh_token"
        }

        data = use_case.execute(request_model=request_data or {})
        assert data["http_status_code"] == 200
        assert data["result"] == {
            "result": {
                "access": {
                    "token": "cca4eb1fa7a244d42895e1f1dd7f89253928b0e65db7d99e692e8f253778c3af",
                    "expire": "2021-12-29T10:24:35"
                },
                "refresh": {
                    "token": "f2301ecdc55a568264d9d7b32c0f1cf36719d1c72a409e1488090bd9fae6b180",
                    "expire": "2021-12-29T18:14:35"
                }
            }
        }
