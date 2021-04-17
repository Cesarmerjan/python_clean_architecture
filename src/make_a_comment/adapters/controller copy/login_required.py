from typing import Union
import traceback
import functools

from src.make_a_comment.exceptions.access_token_required import AccessTokenRequired
from jwt.exceptions import DecodeError, InvalidSignatureError, ExpiredSignatureError, InvalidTokenError

from src.make_a_comment.utils.jwt_handler import ACCESS_TOKEN_BLACKLIST, validate_access_token

from src.make_a_comment.adapters.output.basic import BasicOutput

from src.make_a_comment.utils.logging_handler import file_logger


def login_required(func) -> Union[BasicOutput, 'func']:
    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        access_token = kwargs.get("access_token")

        if not access_token:
            args_access_token_index = inspect.getfullargspec(
                func).args.index("access_token")

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

        return func(*args, **kwargs)

    return wrapper
