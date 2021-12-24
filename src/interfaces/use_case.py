import abc

from interfaces.exception import GeneralException


class UseCaseInterface(metaclass=abc.ABCMeta):
    def execute(self, request_model: dict):
        try:
            return self.process_request(request_model)
        except GeneralException as ex:
            return ex.response()
        except Exception as ex:
            raise ex

    @abc.abstractmethod
    def process_request(self, request_dict: dict) -> dict:
        pass
