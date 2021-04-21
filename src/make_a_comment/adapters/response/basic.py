from typing import Union, List
from .type import ResponseType


class Response(ResponseType):
    def __init__(self, kind: ResponseType, message: str, payload: Union[dict, List[dict]]):
        self.kind = kind
        self.message = self._format_message(message)
        self.payload = payload

    def __str__(self):
        return f"{self.kind}\n{self.message}\n{self.payload}"

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, str(msg))
        return msg

    @classmethod
    def sucess(cls, message=None, payload={}):
        return cls(cls.SUCCESS, message, payload)

    @classmethod
    def created(cls, message=None, payload={}):
        return cls(cls.CREATED, message, payload)

    @classmethod
    def bad_request(cls, message, payload={}):
        return cls(cls.BAD_REQUEST, message, payload)

    @classmethod
    def unauthorized(cls, message, payload={}):
        return cls(cls.UNAUTHORIZED, message, payload)

    @classmethod
    def not_found(cls, message, payload={}):
        return cls(cls.NOT_FOUND, message, payload)

    @classmethod
    def internal_server_error(cls, message, payload={}):
        return cls(cls.INTERNAL_SERVER_ERROR, message, payload)
