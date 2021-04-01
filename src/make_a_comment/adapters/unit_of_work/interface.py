import abc
from src.make_a_comment.adapters.repository.interface import RepositoryInterface


class UoWInterface(metaclass=abc.ABCMeta):
    repository: RepositoryInterface

    def __enter__(self) -> "UoWInterface":
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
