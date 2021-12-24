import abc

from pydantic.main import BaseModel


class ValidatorInterface(BaseModel, metaclass=abc.ABCMeta):
    class Config:
        arbitrary_types_allowed = True
