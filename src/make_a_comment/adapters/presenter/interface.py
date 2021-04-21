import abc
from typing import Any

from src.make_a_comment.adapters.response.basic import Response

from src.make_a_comment.adapters.response.custom_typing import PositiveResponse


class PresenterInterface:

    @abc.abstractmethod
    def build_response(self, function, positive_response: PositiveResponse) -> Response:
        raise NotImplementedError
