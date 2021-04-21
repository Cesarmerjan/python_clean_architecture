from typing import Union
from .type import ResponseType

PositiveResponse = Union[ResponseType.CREATED, ResponseType.SUCCESS]
NegativeResponse = Union[ResponseType.BAD_REQUEST,
                         ResponseType.UNAUTHORIZED,
                         ResponseType.NOT_FOUND,
                         ResponseType.INTERNAL_SERVER_ERROR]
