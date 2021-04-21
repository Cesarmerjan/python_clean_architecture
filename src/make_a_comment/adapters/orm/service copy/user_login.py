from copy import deepcopy
from src.make_a_comment.domain.user import User
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from src.make_a_comment.utils.jwt_handler import generate_access_token
from src.make_a_comment.exceptions.invalid_login_credentials import InvalidLoginCredentials
from .verify_user_password import verify_user_password


def user_login(email: "User.email", password: str, user_uow: UoWInterface) -> str:
    with user_uow:
        user = user_uow.repository.get_by(email=email)

        if not verify_user_password(user.password_hash, password):
            raise InvalidLoginCredentials

        payload = {"user_uuid": user.uuid}

        access_token = generate_access_token(payload)

    return access_token
