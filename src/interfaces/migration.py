import abc


class MigrationInterface(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def up(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def down(cls):
        pass
