import abc
from typing import List


class RepositoryInterface(metaclass=abc.ABCMeta):
    def add(self, object: object) -> None:
        raise NotImplementedError

    def get_by(self, **kwargs) -> object:
        raise NotImplementedError

    def get_all(self) -> List[object]:
        raise NotImplementedError

    def delete(self, **kwargs) -> None:
        raise NotImplementedError

    def update(self, **kwargs) -> object:
        raise NotImplementedError
