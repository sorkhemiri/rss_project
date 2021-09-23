from functools import wraps

from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from entities import User
from repositories.postgres import UserRepository
from repositories.redis import UserAuthenticate


def check_authentication(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        auth_bearer_token = request.META.get("HTTP_AUTHORIZATION")
        if auth_bearer_token:
            auth_token = auth_bearer_token.replace("Bearer ", "")
            user_id = UserAuthenticate.is_authenticated(token=auth_token)
            if user_id:
                if not UserRepository.check_user_exist(user_id=user_id):
                    return JSONResponse(
                        {"error": "این کابر رو نتونستیم پیداش کنیم!"}, status_code=HTTP_401_UNAUTHORIZED
                    )
                user = User(id=user_id)
            else:
                return JSONResponse(
                    {"error": "مطمئنی با کلید درستی داری وارد میشی؟!"}, status_code=HTTP_401_UNAUTHORIZED
                )
        else:
            return JSONResponse(
                {"error": "همچین کلیدی رو پیدا نکردیم!"}, status_code=HTTP_401_UNAUTHORIZED
            )
        return func(request, user=user, *args, **kwargs)

    return inner
