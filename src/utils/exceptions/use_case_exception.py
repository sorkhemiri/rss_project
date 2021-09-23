from .general_exception import GeneralException


class UseCaseException(GeneralException):
    def __init__(self, message: str, error_code: int = 1):
        super(UseCaseException, self).__init__(message=message, error_code=error_code)

    def generate_response_data(self) -> dict:
        exp_data = {
            "error": "UseCase Exception",
            "message": self.message,
            "type": self.code_reference[self.error_code]
            if self.error_code in self.code_reference
            else self.error_code,
        }
        return exp_data
