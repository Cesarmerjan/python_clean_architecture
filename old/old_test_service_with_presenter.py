import contextlib
import pytest

from sqlalchemy.orm.exc import DetachedInstanceError
from jwt.exceptions import DecodeError

from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.domain.user import User

# from src.make_a_comment.use_case import service
from src.make_a_comment.use_case.service.user import UserService
from src.make_a_comment.use_case.service.comment import CommentService


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


def test_can_user_service_register_user(user_data, session_factory):
    session = session_factory()
    user_uow = UserUoW(session_factory)
    user_service = UserService(user_uow)
    user = user_service.register_user(**user_data)
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]

    queried_user = session.query(User).filter_by(uuid=user.uuid).first()

    assert queried_user == user

    session.delete(queried_user)
    session.commit()


def test_can_user_service_make_a_comment(user_data, session_factory):

    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)
        user_service = UserService(user_uow)
        text = "test_can_user_service_make_a_comment"
        comment = user_service.make_a_comment(
            user_uuid=user.uuid, text=text)
        assert comment in user.comments


def test_can_comment_service_get_a_comment_by_uuid(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:

        user_uow = UserUoW(session_factory=session_factory)
        user_service = UserService(user_uow)

        text = "test_can_comment_service_get_a_comment_by_uuid"

        comment = user_service.make_a_comment(
            user_uuid=user.uuid, text=text)

        comment_uow = CommentUoW(session_factory=session_factory)
        comment_service = CommentService(comment_uow)

        queried_comment = comment_service.get_comment_by_uuid(
            comment_uuid=comment.uuid)

        assert queried_comment == comment


def test_can_comment_service_delete_a_comment(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:

        user_uow = UserUoW(session_factory=session_factory)
        user_service = UserService(user_uow)

        initial_numer_of_comments = len(user.comments)
        text = "test_can_comment_service_delete_a_comment"
        comment = user_service.make_a_comment(
            user_uuid=user.uuid, text=text)

        comment_uow = CommentUoW(session_factory=session_factory)
        comment_service = CommentService(comment_uow)

        comment_service.delete_comment_by_uuid(
            comment_uuid=comment.uuid)

        assert len(user.comments) == initial_numer_of_comments


def test_can_comment_service_update_a_comment(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)
        user_service = UserService(user_uow)

        text = "test_can_comment_service_update_a_comment"
        comment = user_service.make_a_comment(
            user_uuid=user.uuid, text=text)

        comment_uow = CommentUoW(session_factory=session_factory)
        comment_service = CommentService(comment_uow)

        new_text = text + " updated"
        new_comment = comment_service.update_comment_by_uuid(
            comment_uuid=comment.uuid, new_text=new_text)

        queried_comment = comment_service.get_comment_by_uuid(
            comment_uuid=comment.uuid)

        assert queried_comment.text == new_text


def test_can_user_service_get_user_by_uuid(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)
        user_service = UserService(user_uow)

        queried_user = user_service.get_user_by_uuid(user_uuid=user.uuid)
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
    comment_service = CommentService(comment_uow)

    queried_comments = comment_service.get_all_comments()

    assert len(comments) == len(queried_comments)


def test_can_service_make_a_user_login(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)
        user_service = UserService(user_uow)

        access_token = user_service.login(
            email=user.email, password=user_data["password"])

        assert validate_access_token(access_token)

        with pytest.raises(InvalidLoginCredentials):
            user_service.login(
                email=user.email, password="wrong")


def test_can_service_verify_user_password(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:
        assert UserService.verify_user_password(
            user.password_hash, user_data["password"])

        assert not UserService.verify_user_password(
            user.password_hash, "wrong")
