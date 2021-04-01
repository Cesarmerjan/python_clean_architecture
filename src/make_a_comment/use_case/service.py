from copy import deepcopy
from typing import List
from werkzeug.security import check_password_hash

from make_a_comment.exceptions.invalid_login_credentials import InvalidLoginCredentials

from src.make_a_comment.utils.jwt_handler import (generate_access_token,
                                                  get_jwt_payload,
                                                  validate_access_token,
                                                  ACCESS_TOKEN_BLACKLIST,
                                                  get_jwt_identity)

from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface


def create_a_user(name: str, email: str, password: str, user_uow: UoWInterface) -> User:
    with user_uow:
        user = user_uow.repository.add(
            User(name, email, password)
        )
        response = deepcopy(user)
        user_uow.commit()
    return response


def make_a_user_comment(user_uuid: "User.uuid", text: str, user_uow: UoWInterface) -> Comment:
    with user_uow:
        user = user_uow.repository.get_by(uuid=user_uuid)
        comment = Comment(text)
        response = deepcopy(comment)
        user.make_a_comment(comment)
        user_uow.repository.add(user)
        user_uow.commit()
    return response


def get_a_comment_by_uuid(comment_uuid: "Comment.uuid", comment_uow: UoWInterface) -> Comment:
    with comment_uow:
        comment = comment_uow.repository.get_by(uuid=comment_uuid)
        response = deepcopy(comment)
    return response


def delete_a_comment_by_uuid(comment_uuid: "Comment.uuid", comment_uow: UoWInterface) -> None:
    with comment_uow:
        comment = comment_uow.repository.get_by(uuid=comment_uuid)
        comment_uow.repository.delete(comment)
        comment_uow.commit()


def update_a_comment(comment_uuid: "Comment.uuid", new_text: str, comment_uow: UoWInterface) -> Comment:
    with comment_uow:
        comment = comment_uow.repository.get_by(uuid=comment_uuid)
        comment.text = new_text
        response = deepcopy(comment)
        comment_uow.repository.add(comment)
        comment_uow.commit()
        return response


def get_a_user_by_uuid(user_uuid: "User.uuid", user_uow: UoWInterface):
    with user_uow:
        user = user_uow.repository.get_by(uuid=user_uuid)
        # This (user.comments) needs to be here because of the relationship
        # This query all comments of the user before creating the deepcopy
        # If this is not here you will get the following error:
        # sqlalchemy.orm.exc.DetachedInstanceError
        user.comments
        response = deepcopy(user)
    return response


def view_all_comments(comment_uow: UoWInterface) -> List[Comment]:
    with comment_uow:
        comments = comment_uow.repository.get_all()
        response = deepcopy(comments)
    return response


def user_login(email: "User.email", password: str, user_uow: UoWInterface) -> str:
    with user_uow:
        user = user_uow.repository.get_by(email=email)

        if not verify_user_password(user.password_hash, password):
            raise InvalidLoginCredentials

        payload = {"user_uuid": user.uuid}

        access_token = generate_access_token(payload)

    return access_token


def user_logout(access_token):
    ACCESS_TOKEN_BLACKLIST.add(access_token)


def verify_access_token(access_token):
    return validate_access_token(access_token)


def verify_user_password(user_password_hash: "User.password_hash", password: str) -> bool:
    return check_password_hash(user_password_hash, password)


def get_payload_from_jwt(access_token):
    payload = get_jwt_payload(access_token)
    return payload


def get_jti_from_jwt(access_token):
    jti = get_jwt_identity(access_token)
    return jti
