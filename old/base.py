from typing import List
from .exception import RequestDataException


class BaseRequestDataParser:

    def __init__(self, request_data: dict):
        self.request_exceptions = []  # type: List[RequestDataException]
        self._request_data = None
        self.request_data = request_data

    def __str__(self):
        return f"request_data: {self.request_data}\nrequest_exceptions: {self.request_exceptions}"

    @property
    def request_data_is_valid(self) -> bool:
        if not self.request_exceptions:
            return True
        else:
            return False

    @property
    def request_data(self) -> dict:
        return self._request_data

    @request_data.setter
    def request_data(self, request_data: dict) -> None:
        self.request_exceptions += self._validate_request_data(
            request_data)
        self._request_data = request_data

    @staticmethod
    def _validate_request_data(request_data: dict) -> List[RequestDataException]:
        raise NotImplementedError

    @property
    def request_exceptions_messages(self):
        return " and ".join(map(str, self.request_exceptions))
