import abc
from exceptions import (
    GeneralException,
    UseCaseException,
    RepositoryException,
    EntityException,
)


class UseCaseInterface(metaclass=abc.ABCMeta):
    def execute(self, request_model: dict):
        try:
            return self.process_request(request_model)
        except (
            GeneralException,
            UseCaseException,
            RepositoryException,
            EntityException,
        ) as ex:
            return ex.response()
        except Exception as ex:
            raise ex

    @abc.abstractmethod
    def process_request(self, request_dict: dict):
        pass
