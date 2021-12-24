from interfaces.exception import GeneralException
from exceptions import error_status


class EntityException(GeneralException):
    def __init__(self, message: str, error_code: int = error_status.GENERAL_ERROR):
        super(EntityException, self).__init__(message=message, error_code=error_code)

    def response(self) -> dict:
        self.exception_data["error"] = "Entity Exception"
        return self.exception_data
