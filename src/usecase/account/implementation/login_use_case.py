import orjson as json
from pydantic import ValidationError
from starlette.responses import JSONResponse

from usecase.interface import UseCaseInterface
# from desk.validators import BookmarkPostValidator
# from repositories.postgres import (
#     PostRepository,
#     BookmarkRepository,
# )
from utils.exceptions import UseCaseException, status


class LoginUseCase(UseCaseInterface):
    def process_request(self, request_dict: dict):
        try:
            return JSONResponse(content={"result": "ok"})
        except ValidationError as err:
            raise UseCaseException(json.loads(err.json()), error_code=2)
        except UseCaseException as err:
            raise err
