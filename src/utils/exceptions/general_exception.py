from abc import abstractmethod
import inspect

from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from . import status


class GeneralException(Exception):
    def __init__(self, message: str, error_code: int = 0):

        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.code_reference = self.load_code_reference()
        print(self.code_reference)

    @abstractmethod
    def generate_response_data(self):
        pass

    def response(self) -> JSONResponse:
        data = self.generate_response_data()
        if self.error_code == status.DOES_NOT_EXIST_ERROR:
            return JSONResponse(content=data, status_code=HTTP_404_NOT_FOUND)
        elif self.error_code == status.AUTHORIZATION_ERROR:
            return JSONResponse(content=data, status_code=HTTP_401_UNAUTHORIZED)
        else:
            return JSONResponse(content=data, status_code=HTTP_400_BAD_REQUEST)

    @staticmethod
    def load_code_reference():
        code_reference = {}
        for name, obj in inspect.getmembers(status):
            if inspect.isclass(obj):
                code_reference.update({obj.error_code: obj.message})
        return code_reference
