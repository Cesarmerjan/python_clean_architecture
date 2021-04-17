import abc


class InputInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError
