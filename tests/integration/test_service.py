import contextlib
import pytest

from sqlalchemy.orm.exc import DetachedInstanceError
from jwt.exceptions import DecodeError

from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.domain.user import User

from src.make_a_comment.use_case import service

from src.make_a_comment.utils.jwt_handler import validate_access_token

from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW

from src.make_a_comment.exceptions.invalid_login_credentials import InvalidLoginCredentials


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


def test_can_service_create_a_user(user_data, session_factory):
    session = session_factory()
    user_uow = UserUoW(session_factory)
    user = service.create_a_user(**user_data, user_uow=user_uow)
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]

    queried_user = session.query(User).filter_by(uuid=user.uuid).first()

    assert queried_user == user

    session.delete(queried_user)
    session.commit()


def test_can_service_make_a_user_comment(user_data, session_factory):

    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)
        text = "test_can_service_make_an_user_comment"
        comment = service.make_a_user_comment(
            user_uuid=user.uuid, text=text, user_uow=user_uow)
        assert comment in user.comments


def test_can_service_get_a_comment_by_uuid(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:

        user_uow = UserUoW(session_factory=session_factory)

        text = "test_can_service_get_a_comment_by_uuid"

        comment = service.make_a_user_comment(
            user_uuid=user.uuid, text=text, user_uow=user_uow)

        comment_uow = CommentUoW(session_factory=session_factory)

        queried_comment = service.get_a_comment_by_uuid(
            comment_uuid=comment.uuid, comment_uow=comment_uow)

        assert queried_comment == comment


def test_can_service_delete_a_comment(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:

        user_uow = UserUoW(session_factory=session_factory)
        initial_numer_of_comments = len(user.comments)
        text = "test_can_service_delete_a_user_comment"
        comment = service.make_a_user_comment(
            user_uuid=user.uuid, text=text, user_uow=user_uow)

        comment_uow = CommentUoW(session_factory=session_factory)

        service.delete_a_comment_by_uuid(
            comment_uuid=comment.uuid, comment_uow=comment_uow)

        assert len(user.comments) == initial_numer_of_comments


def test_can_service_update_a_comment(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)
        text = "test_can_service_update_a_comment"
        comment = service.make_a_user_comment(
            user_uuid=user.uuid, text=text, user_uow=user_uow)

        comment_uow = CommentUoW(session_factory=session_factory)

        new_text = text + " updated"
        new_comment = service.update_a_comment(
            comment_uuid=comment.uuid, new_text=new_text,
            comment_uow=comment_uow)

        queried_comment = service.get_a_comment_by_uuid(
            comment_uuid=comment.uuid, comment_uow=comment_uow)

        assert queried_comment.text == new_text


def test_can_service_get_a_user_by_uuid(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)

        queried_user = service.get_a_user_by_uuid(user_uuid=user.uuid,
                                                  user_uow=user_uow)
        assert queried_user == user

        try:
            queried_user.comments
        except DetachedInstanceError:
            pytest.fail("insert user.comments berofore deepcopy user")


def test_can_service_view_all_comments(session_factory):
    session = session_factory()
    comments = session.query(Comment).all()
    session.close()
    comment_uow = CommentUoW(session_factory=session_factory)

    queried_comments = service.view_all_comments(comment_uow=comment_uow)

    assert len(comments) == len(queried_comments)


def test_can_service_make_a_user_login(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)

        access_token = service.user_login(
            email=user.email, password=user_data["password"],
            user_uow=user_uow)

        assert validate_access_token(access_token)

        with pytest.raises(InvalidLoginCredentials):
            service.user_login(
                email=user.email, password="wrong",
                user_uow=user_uow)


# def test_can_service_get_payload_from_jwt(user_data, session_factory):
#     with create_a_user_and_persist_it(user_data, session_factory) as user:
#         user_uow = UserUoW(session_factory=session_factory)

#         access_token = service.user_login(
#             email=user.email, password=user_data["password"],
#             user_uow=user_uow)

#         payload = service.get_payload_from_jwt(access_token)
#         user_uuid = payload["user_uuid"]
#         assert user_uuid == user.uuid

#         with pytest.raises(DecodeError):
#             service.get_payload_from_jwt("wrong")


def test_can_service_verify_user_password(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:
        assert service.verify_user_password(
            user.password_hash, user_data["password"])

        assert not service.verify_user_password(
            user.password_hash, "wrong")


# def test_can_service_verify_access_token(user_data, session_factory):
#     with create_a_user_and_persist_it(user_data, session_factory) as user:
#         user_uow = UserUoW(session_factory=session_factory)

#         access_token = service.user_login(
#             email=user.email, password=user_data["password"],
#             user_uow=user_uow)

#         assert service.verify_access_token(access_token)

#         with pytest.raises(DecodeError):
#             service.verify_access_token("wrong")
