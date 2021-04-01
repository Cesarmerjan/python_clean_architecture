import uuid
import functools
import inspect
from typing import NewType
from datetime import datetime
import jwt

from src.make_a_comment.exceptions.access_token_required import AccessTokenRequired

from src.config import SECRET_KEY

Seconds = NewType("Seconds", int)

ACCESS_TOKEN_BLACKLIST = set()

JWT_RESERVED_CLAIMS = ["iss", "sub", "aud", "exp", "nbf", "iat", "jti"]


def generate_access_token(payload, time_to_expire: Seconds = None) -> str:
    if time_to_expire:
        payload["exp"] = datetime.utcnow(
        ) + datetime.timedelta(seconds=time_to_expire)
    payload["iat"] = datetime.utcnow()
    payload["jti"] = str(uuid.uuid4())
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def validate_access_token(access_token) -> dict:
    if access_token in ACCESS_TOKEN_BLACKLIST:
        raise jwt.exceptions.InvalidTokenError
    try:
        return jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError as error:
        raise error
    except jwt.exceptions.ExpiredSignatureError as error:
        raise error
    except jwt.exceptions.DecodeError as error:
        raise error


def get_jwt_payload(access_token) -> dict:
    try:
        payload = jwt.decode(access_token, options={"verify_signature": False})
    except jwt.exceptions.DecodeError as error:
        raise error

    payload = {
        key: value
        for (key, value) in payload.items()
        if key not in JWT_RESERVED_CLAIMS
    }
    return payload


def get_jwt_identity(access_token):
    try:
        payload = jwt.decode(access_token, options={"verify_signature": False})
    except jwt.exceptions.DecodeError as error:
        raise error
    return payload.get("jti")


def login_required(func):
    @functools.wraps(func)
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
            raise jwt.exceptions.InvalidTokenError

        validate_access_token(access_token)

        return func(*args, **kwargs)

    return wrapper
