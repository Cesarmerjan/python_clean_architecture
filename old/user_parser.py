from typing import List
from marshmallow.exceptions import ValidationError
from .exception import RequestDataException
from .base import BaseRequestDataParser

from src.make_a_comment.adapters.serializer.user import user_serializer


class UserRequestParser(BaseRequestDataParser):

    @staticmethod
    def _validate_request_data(request_data: dict) -> List[RequestDataException]:
        errors = []
        try:
            user_serializer.load(request_data)
        except ValidationError as error:
            for key, value in error.messages.items():
                errors.append(RequestDataException(key, " and ".join(value)))
        return errors
