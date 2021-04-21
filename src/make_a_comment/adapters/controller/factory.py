from src.make_a_comment.adapters.request.basic import Request
from src.make_a_comment.adapters.response.basic import Response
from src.make_a_comment.adapters.presenter.basic import Presenter

from src.make_a_comment.adapters.serializer.access_token import AccessTokenSchema
from src.make_a_comment.adapters.serializer.user import UserSerializer
from src.make_a_comment.adapters.serializer.comment import CommentSerializer

from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW
from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW

from src.make_a_comment.use_case.service.user import UserService
from src.make_a_comment.use_case.service.comment import CommentService

from .delete_a_comment_by_uuid import DeleteCommentController
from .get_all_comments import GetAllCommentsController
from .get_comment_by_uuid import GetCommentController
from .get_user_by_uuid import GetUserController
from .make_a_comment import MakeACommentController
from .register_user import RegisterUserController
from .update_a_comment import UpdateCommentController
from .user_login import UserLoginController
from .user_logout import UserLogoutController


class ControllerFactory:

    registered_controllers = {

        "get_all_comments": GetAllCommentsController(
            CommentService(
                CommentUoW(None), Presenter(CommentSerializer())
            )
        ),

        "get_comment_by_uuid": GetCommentController(
            CommentService(
                CommentUoW(None), Presenter(CommentSerializer())
            )
        ),

        "update_a_comment": UpdateCommentController(
            CommentService(
                CommentUoW(None), Presenter(CommentSerializer())
            )
        ),

        "delete_a_comment_by_uuid": DeleteCommentController(
            CommentService(
                CommentUoW(None), Presenter(CommentSerializer())
            )
        ),

        "register_user": RegisterUserController(
            UserService(
                UserUoW(None), Presenter(UserSerializer())
            )
        ),
        "maka_a_comment": MakeACommentController(
            UserService(
                user_uow=UserUoW(None), presenter=Presenter(CommentSerializer())
            )
        ),

        "get_user_by_uuid": GetUserController(
            UserService(
                UserUoW(None), Presenter(UserSerializer())
            )
        ),

        "user_login": UserLoginController(
            UserService(
                UserUoW(None), Presenter(AccessTokenSchema())
            )
        ),

        "user_logout": UserLogoutController(
            UserService(
                UserUoW(None), Presenter(AccessTokenSchema())
            )
        )

    }

    def __init__(self, controller_name: str, session_factory):
        self.controller = self.set_controller(
            controller_name, session_factory)

    def set_controller(self, controller_name, session_factory):
        controller = self.registered_controllers[controller_name]
        controller.service.uow.session_factory = session_factory
        return controller

    def handle(self, data: dict):
        return self.controller.handle(Request(data))
