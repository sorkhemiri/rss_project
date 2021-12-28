import abc
import inspect

from exceptions import error_status


class GeneralException(Exception):
    CODE_REFERENCE = None

    def __init__(self, message: str, error_code: int = error_status.GENERAL_ERROR):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        if not self.CODE_REFERENCE:
            self.CODE_REFERENCE = self.load_code_reference()
        self.exception_data = self.load_response()

    def load_response(self):
        exception = (
            self.CODE_REFERENCE[self.error_code]
            if self.error_code in self.CODE_REFERENCE
            else self.CODE_REFERENCE[error_status.GENERAL_ERROR]
        )
        exception_data = {
            "message": self.message,
            "type": exception.message,
            "http_status_code": exception.status_code,
        }
        return exception_data

    @abc.abstractmethod
    def response(self) -> dict:
        pass

    @classmethod
    def load_code_reference(cls):
        code_reference = {}
        for name, obj in inspect.getmembers(error_status):
            if inspect.isclass(obj):
                code_reference.update({obj.error_code: obj})

        return code_reference
