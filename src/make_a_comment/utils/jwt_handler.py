from typing import NewType
import functools
import inspect
import jwt
from config import SECRET_KEY

Seconds = NewType("Seconds", int)


def generate_access_token(pay_load, time_to_expire: Seconds = None) -> str:
    if time_to_expire:
        pay_load["exp"] = time.time() + time_to_expire
    return jwt.encode(pay_load, SECRET_KEY, algorithm="HS256")


def validate_access_token(access_token) -> dict:
    try:
        return jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError:
        raise jwt.exceptions.InvalidSignatureError
    except jwt.exceptions.ExpiredSignatureError:
        raise jwt.exceptions.ExpiredSignatureError


def get_jwt_pay_load(access_token) -> dict:
    pay_load = jwt.decode(access_token, options={"verify_signature": False})
    if pay_load.get("exp"):
        del pay_load["exp"]
    return pay_load


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
            raise ValueError("Access token required")

        validate_access_token(access_token)

        return func(*args, **kwargs)

    return wrapper
