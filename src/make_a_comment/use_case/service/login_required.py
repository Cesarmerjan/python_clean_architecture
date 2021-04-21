import inspect
from functools import wraps

import jwt

from src.make_a_comment.exceptions.access_token_required import AccessTokenRequired
from jwt.exceptions import DecodeError, InvalidSignatureError, ExpiredSignatureError, InvalidTokenError

from src.make_a_comment.utils.jwt_handler import ACCESS_TOKEN_BLACKLIST, validate_access_token

ACCESS_TOKEN_NAME: str = "access_token"


def login_required(function) -> callable:
    @wraps(function)
    def wrapper(*args, **kwargs):
        access_token = kwargs.get(ACCESS_TOKEN_NAME)

        if not access_token:
            args_access_token_index = inspect.getfullargspec(
                function).args.index(ACCESS_TOKEN_NAME)

            if not args_access_token_index >= len(args):
                access_token = args[args_access_token_index]

        if not access_token:
            raise AccessTokenRequired

        if access_token in ACCESS_TOKEN_BLACKLIST:
            raise InvalidTokenError

        try:
            validate_access_token(access_token)
        except jwt.exceptions.InvalidSignatureError as error:
            raise error
        except jwt.exceptions.ExpiredSignatureError as error:
            raise error
        except jwt.exceptions.DecodeError as error:
            raise error

        return function(*args, **kwargs)

    return wrapper
