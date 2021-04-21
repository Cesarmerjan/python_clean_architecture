import contextlib

from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.domain.user import User

from src.make_a_comment.utils.jwt_handler import ACCESS_TOKEN_BLACKLIST
from src.make_a_comment.utils.jwt_handler import validate_access_token

from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW
from src.make_a_comment.use_case.service.comment import CommentService

from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW
from src.make_a_comment.use_case.service.user import UserService


from src.make_a_comment.adapters.controller import (RegisterUserController,
                                                    GetUserController,
                                                    GetAllCommentsController,
                                                    UserLoginController,
                                                    MakeACommentController,
                                                    GetCommentController,
                                                    UpdateCommentController,
                                                    DeleteCommentController,
                                                    UserLogoutController)

from src.make_a_comment.adapters.response.type import ResponseType
from src.make_a_comment.adapters.request.basic import Request

from src.make_a_comment.adapters.presenter.basic import Presenter

from src.make_a_comment.adapters.serializer.comment import CommentSerializer
from src.make_a_comment.adapters.serializer.user import UserSerializer
from src.make_a_comment.adapters.serializer.access_token import AccessTokenSchema


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


def test_can_controller_register_user(user_data, session_factory):
    data = user_data
    session = session_factory()

    user_uow = UserUoW(session_factory)

    presenter = Presenter(UserSerializer())

    user_service = UserService(user_uow, presenter)
    register_user_controller = RegisterUserController(user_service)

    request = Request(data)
    response = register_user_controller.handle(request=request)

    assert response.kind == ResponseType.CREATED

    assert response.payload["name"] == user_data["name"]
    assert response.payload["email"] == user_data["email"]

    queried_user = session.query(User).filter_by(
        uuid=response.payload["uuid"]).first()

    assert queried_user.uuid == response.payload["uuid"]
    assert queried_user.name == response.payload["name"]
    assert queried_user.email == response.payload["email"]

    session.delete(queried_user)
    session.commit()


def test_can_controller_make_a_comment(user_data, session_factory):

    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)

        presenter = Presenter(AccessTokenSchema())

        user_service = UserService(user_uow, presenter)

        user_login_controller = UserLoginController(user_service)

        data = {"email": user.email,
                "password": user_data["password"]}

        request = Request(data)

        response = user_login_controller.handle(request=request)

        access_token = response.payload["access_token"]

        user_service.presenter.serializer = CommentSerializer()

        make_a_comment_controller = MakeACommentController(user_service)

        data = {"user_uuid": user.uuid,
                "text": "test_can_controller_make_an_user_comment",
                "access_token": access_token}

        request = Request(data)

        response = make_a_comment_controller.handle(request=request)

        assert response.kind == ResponseType.CREATED

        assert len(user.comments) == 1

        for comment in user.comments:
            assert comment.uuid == response.payload["uuid"]
            assert comment.text == response.payload["text"]


def test_can_controller_get_comment_by_uuid(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:

        user_uow = UserUoW(session_factory=session_factory)

        presenter = Presenter(AccessTokenSchema())

        user_service = UserService(user_uow, presenter)

        user_login_controller = UserLoginController(user_service)

        data = {"email": user.email,
                "password": user_data["password"]}

        request = Request(data)

        response = user_login_controller.handle(request=request)

        access_token = response.payload["access_token"]

        # -----------------------------------------------------------

        user_service.presenter.serializer = CommentSerializer()

        make_a_comment_controller = MakeACommentController(user_service)

        data = {"user_uuid": user.uuid,
                "text": "test_can_controller_make_an_user_comment",
                "access_token": access_token}

        request = Request(data)

        response = make_a_comment_controller.handle(request=request)

        comment = response.payload

        # -----------------------------------------------------------

        comment_uow = CommentUoW(session_factory=session_factory)

        presenter = Presenter(CommentSerializer())

        comment_service = CommentService(comment_uow, presenter)

        get_comment_by_uuid_controller = GetCommentController(comment_service)

        data = {"comment_uuid": comment["uuid"],
                "access_token": access_token}

        request = Request(data)

        response = get_comment_by_uuid_controller.handle(request=request)

        assert response.kind == ResponseType.SUCCESS

        assert response.payload["text"] == comment["text"]


def test_can_controller_update_comment(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:

        user_uow = UserUoW(session_factory=session_factory)

        presenter = Presenter(AccessTokenSchema())

        user_service = UserService(user_uow, presenter)

        user_login_controller = UserLoginController(user_service)

        data = {"email": user.email,
                "password": user_data["password"]}

        request = Request(data)

        response = user_login_controller.handle(request=request)

        access_token = response.payload["access_token"]

        # -----------------------------------------------------------

        user_service.presenter.serializer = CommentSerializer()

        make_a_comment_controller = MakeACommentController(user_service)

        data = {"user_uuid": user.uuid,
                "text": "test_can_controller_make_an_user_comment",
                "access_token": access_token}

        request = Request(data)

        response = make_a_comment_controller.handle(request=request)

        comment = response.payload

        # -----------------------------------------------------------

        comment_uow = CommentUoW(session_factory=session_factory)

        presenter = Presenter(CommentSerializer())

        comment_service = CommentService(comment_uow, presenter)

        update_comment_controller = UpdateCommentController(comment_service)

        new_text = data["text"] + " updated"
        data = {"new_text": new_text,
                "comment_uuid": comment["uuid"],
                "access_token": access_token}

        request = Request(data)

        response = update_comment_controller.handle(request=request)

        assert response.kind == ResponseType.SUCCESS
        assert comment["uuid"] == response.payload["uuid"]

        assert response.payload["text"] == data["new_text"]


def test_can_controller_delete_comment(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:

        user_uow = UserUoW(session_factory=session_factory)

        presenter = Presenter(AccessTokenSchema())

        user_service = UserService(user_uow, presenter)

        user_login_controller = UserLoginController(user_service)

        data = {"email": user.email,
                "password": user_data["password"]}

        request = Request(data)

        response = user_login_controller.handle(request=request)

        access_token = response.payload["access_token"]

        # -----------------------------------------------------------

        user_service.presenter.serializer = CommentSerializer()

        make_a_comment_controller = MakeACommentController(user_service)

        data = {"user_uuid": user.uuid,
                "text": "test_can_controller_make_an_user_comment",
                "access_token": access_token}

        request = Request(data)

        response = make_a_comment_controller.handle(request=request)

        comment = response.payload

        # -----------------------------------------------------------

        comment_uow = CommentUoW(session_factory=session_factory)

        presenter = Presenter(CommentSerializer())

        comment_service = CommentService(comment_uow, presenter)

        delete_comment_controller = DeleteCommentController(comment_service)

        data = {"access_token": access_token,
                "comment_uuid": comment["uuid"]}

        request = Request(data)

        response = delete_comment_controller.handle(request=request)

        assert response.kind == ResponseType.SUCCESS


def test_can_controller_get_user_by_uuid(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:
        user_uow = UserUoW(session_factory=session_factory)

        presenter = Presenter(UserSerializer())

        user_service = UserService(user_uow, presenter)

        get_user_controller = GetUserController(user_service)

        data = {"user_uuid": user.uuid}

        request = Request(data)

        response = get_user_controller.handle(request=request)

        assert response.kind == ResponseType.SUCCESS

        assert response.payload["uuid"] == user.uuid
        assert response.payload["name"] == user.name
        assert response.payload["email"] == user.email


def test_can_controller_get_all_comments(session_factory):
    session = session_factory()
    comments = session.query(Comment).all()
    session.close()
    comment_uow = CommentUoW(session_factory=session_factory)

    presenter = Presenter(CommentSerializer(many=True))

    comment_service = CommentService(comment_uow, presenter)

    get_all_comments_controller = GetAllCommentsController(comment_service)

    request = Request({})

    response = get_all_comments_controller.handle(request)

    assert len(comments) == len(response.payload)


def test_can_controller_make_a_user_login(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:

        user_uow = UserUoW(session_factory=session_factory)

        presenter = Presenter(AccessTokenSchema())

        user_service = UserService(user_uow, presenter)

        user_login_controller = UserLoginController(user_service)

        data = {"email": user.email,
                "password": user_data["password"]}

        request = Request(data)

        response = user_login_controller.handle(request=request)

        assert validate_access_token(response.payload["access_token"])
        assert response.kind == ResponseType.SUCCESS


def test_can_controller_make_a_user_logout(user_data, session_factory):
    with create_a_user_and_persist_it(user_data, session_factory) as user:

        user_uow = UserUoW(session_factory=session_factory)

        presenter = Presenter(AccessTokenSchema())

        user_service = UserService(user_uow, presenter)

        user_login_controller = UserLoginController(user_service)

        data = {"email": user.email,
                "password": user_data["password"]}

        request = Request(data)

        response = user_login_controller.handle(request=request)

        assert validate_access_token(response.payload["access_token"])
        assert response.kind == ResponseType.SUCCESS

        # -----------------------------------------------------------

        user_logout_controller = UserLogoutController(user_service)

        data = {"access_token": response.payload["access_token"]}

        request = Request(data)

        response = user_logout_controller.handle(request=request)

        assert response.kind == ResponseType.SUCCESS

        assert data["access_token"] in ACCESS_TOKEN_BLACKLIST
