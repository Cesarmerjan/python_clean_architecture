import uuid
import inspect
from typing import NewType
from datetime import datetime
import jwt

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
    return jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])


def get_jwt_payload(access_token) -> dict:
    payload = jwt.decode(access_token, options={"verify_signature": False})

    payload = {
        key: value
        for (key, value) in payload.items()
        if key not in JWT_RESERVED_CLAIMS
    }
    return payload


def get_jwt_identity(access_token):
    payload = jwt.decode(access_token, options={"verify_signature": False})

    return payload.get("jti")
