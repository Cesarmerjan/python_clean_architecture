import pytest
import contextlib

from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.domain.user import User

from src.make_a_comment.use_case import interactor

from src.make_a_comment.utils.jwt_handler import validate_access_token

from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from jwt.exceptions import DecodeError, InvalidSignatureError, ExpiredSignatureError, InvalidTokenError
from make_a_comment.exceptions.invalid_login_credentials import InvalidLoginCredentials
from make_a_comment.exceptions.user_uuid_is_not_in_the_access_token_payload import UserUuidIsNotInAccessTokenPayload
from make_a_comment.exceptions.missing_data_on_request import (
    MissingCommentUuid,
    MissingNewCommentText,
    MissingUserUuid,
    MissingUserEmail,
    MissingUserPassword)


@contextlib.contextmanager
def create_a_user_and_persist_it(user_data, session_factory):
    session = session_factory()
    user = User(**user_data)
    session.add(user)
    session.commit()
    try:
        yield user
    finally:
        session.delete(user)
        session.commit()
        session.close()


# with pytest.raises(IntegrityError):
#     user_repository.add(User(**user_data))
#     assert session.commit()
# session.rollback()

# def test_can_interactor_create_a_user(user_data, session_factory):
#     request_json = user_data
#     session = session_factory()
#     user_uow = UserUoW(session_factory)

#     with pytest.raises(ValidationError):
#         response = interactor.create_a_user(
#             request_json={}, user_uow=user_uow)
#     session.rollback()

#     with pytest.raises(ValidationError):
#         response = interactor.create_a_user(
#             request_json={"wrong": "wrong"}, user_uow=user_uow)
#     session.rollback()

#     with pytest.raises(ValidationError):
#         response = interactor.create_a_user(
#             request_json={"email": "email"}, user_uow=user_uow)
#     session.rollback()

#     with pytest.raises(ValidationError):
#         response = interactor.create_a_user(
#             request_json={"password": "five"}, user_uow=user_uow)
#     session.rollback()

#     user = interactor.create_a_user(
#         request_json=request_json, user_uow=user_uow)
#     with pytest.raises(IntegrityError):
#         interactor.create_a_user(request_json=request_json, user_uow=user_uow)
#     session.rollback()

#     queried_user = session.query(User).filter_by(uuid=user["uuid"]).first()

#     session.delete(queried_user)
#     session.commit()


# def test_can_interactor_make_a_user_comment(user_data, session_factory):

#     with create_a_user_and_persist_it(user_data, session_factory) as user:
#         user_uow = UserUoW(session_factory=session_factory)

#         request_json = {"email": user.email,
#                         "password": user_data["password"]}

#         access_token = interactor.user_login(request_json=request_json,
#                                              user_uow=user_uow)

#         request_json = {"text": "test_can_interactor_make_an_user_comment"}
#         response = interactor.make_a_user_comment(
#             request_json=request_json, user_uow=user_uow,
#             access_token="wrong")

        # assert len(user.comments) == 1

        # for comment in user.comments:
        #     assert comment.uuid == response["uuid"]
        #     assert comment.text == response["text"]

# def test_can_interactor_get_a_comment_by_uuid(user_data, session_factory):
#     with create_a_user_and_persist_it(user_data, session_factory) as user:

#         user_uow = UserUoW(session_factory=session_factory)

#         request_json = {"email": user.email,
#                         "password": user_data["password"]}

#         access_token = interactor.user_login(request_json=request_json,
#                                              user_uow=user_uow)

#         request_json = {"text": "test_can_interactor_get_a_comment_by_uuid"}
#         comment = interactor.make_a_user_comment(
#             request_json, user_uow=user_uow, access_token=access_token)

#         comment_uow = CommentUoW(session_factory=session_factory)

#         request_json = {"comment_uuid": comment["uuid"]}

#         queried_comment = interactor.get_a_comment_by_uuid(
#             request_json, comment_uow=comment_uow)

#         assert queried_comment == comment

# def test_can_interactor_delete_a_comment(user_data, session_factory):
#     with create_a_user_and_persist_it(user_data, session_factory) as user:

#         user_uow = UserUoW(session_factory=session_factory)

#         request_json = {"email": user.email,
#                         "password": user_data["password"]}

#         access_token = interactor.user_login(request_json=request_json,
#                                              user_uow=user_uow)

#         initial_numer_of_comments = len(user.comments)
#         request_json = {"text": "test_can_interactor_delete_a_user_comment"}
#         response = interactor.make_a_user_comment(
#             request_json=request_json,
#             user_uow=user_uow,
#             access_token=access_token)

#         request_json = {"comment_uuid": response["uuid"]}
#         comment_uow = CommentUoW(session_factory=session_factory)

#         interactor.delete_a_comment_by_uuid(
#             request_json=request_json, comment_uow=comment_uow,
#             access_token=access_token)

#         assert len(user.comments) == initial_numer_of_comments

# def test_can_interactor_update_a_comment(user_data, session_factory):
#     with create_a_user_and_persist_it(user_data, session_factory) as user:
#         user_uow = UserUoW(session_factory=session_factory)

#         request_json = {"email": user.email,
#                         "password": user_data["password"]}

#         access_token = interactor.user_login(request_json=request_json,
#                                              user_uow=user_uow)

#         request_json = {"text": "test_can_interactor_update_a_comment"}
#         response = interactor.make_a_user_comment(
#             request_json=request_json, user_uow=user_uow,
#             access_token=access_token)

#         comment_uow = CommentUoW(session_factory=session_factory)

#         new_text = request_json["text"] + " updated"
#         request_json = {"new_text": new_text,
#                         "comment_uuid": response["uuid"]}
#         new_comment = interactor.update_a_comment(
#             request_json=request_json,
#             comment_uow=comment_uow, access_token=access_token)

#         queried_comment = interactor.get_a_comment_by_uuid(
#             request_json={"comment_uuid": response["uuid"]},
#             comment_uow=comment_uow)

#         assert queried_comment["text"] == new_text

# def test_can_interactor_get_a_user_by_uuid(user_data, session_factory):
#     with create_a_user_and_persist_it(user_data, session_factory) as user:
#         user_uow = UserUoW(session_factory=session_factory)

#         request_json = {"user_uuid": user.uuid}

#         queried_user = interactor.get_a_user_by_uuid(request_json=request_json,
#                                                      user_uow=user_uow)

#         assert queried_user["uuid"] == user.uuid
#         assert queried_user["name"] == user.name
#         assert queried_user["email"] == user.email

# def test_can_interactor_view_all_comments(session_factory):
#     session = session_factory()
#     comments = session.query(Comment).all()
#     session.close()
#     comment_uow = CommentUoW(session_factory=session_factory)

#     queried_comments = interactor.view_all_comments(comment_uow=comment_uow)

#     assert len(comments) == len(queried_comments)

# def test_can_interactor_make_a_user_login(user_data, session_factory):
#     with create_a_user_and_persist_it(user_data, session_factory) as user:

#         user_uow = UserUoW(session_factory=session_factory)

#         request_json = {"email": user.email,
#                         "password": user_data["password"]}

#         access_token = interactor.user_login(request_json=request_json,
#                                              user_uow=user_uow)

#         assert validate_access_token(access_token)

# def test_can_interactor_get_payload_from_jwt(user_data, session_factory):
#     with create_a_user_and_persist_it(user_data, session_factory) as user:
#         user_uow = UserUoW(session_factory=session_factory)

#         request_json = {"email": user.email,
#                         "password": user_data["password"]}

#         access_token = interactor.user_login(request_json=request_json,
#                                              user_uow=user_uow)

#         payload = interactor.get_payload_from_jwt(access_token)
#         user_uuid = payload["user_uuid"]
#         assert user_uuid == user.uuid

# def test_can_interactor_verify_user_password(user_data, session_factory):
#     with create_a_user_and_persist_it(user_data, session_factory) as user:
#         assert interactor.verify_user_password(
#             user.password_hash, user_data["password"])
