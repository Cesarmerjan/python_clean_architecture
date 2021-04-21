import functools
from .interface import PresenterInterface

from src.make_a_comment.adapters.response.basic import Response
from src.make_a_comment.adapters.response.type import ResponseType

# acho que o presenter pode recever im serialezer e um deserializer


class FakePresenter(PresenterInterface):

    def build_response(self, function, positive_response=ResponseType.SUCCESS):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
