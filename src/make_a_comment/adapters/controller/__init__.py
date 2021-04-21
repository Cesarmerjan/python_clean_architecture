"""Responsible for directing the request to the business rule"""
from .delete_a_comment_by_uuid import DeleteCommentController
from .get_comment_by_uuid import GetCommentController
from .get_user_by_uuid import GetUserController
from .make_a_comment import MakeACommentController
from .register_user import RegisterUserController
from .update_a_comment import UpdateCommentController
from .user_login import UserLoginController
from .user_logout import UserLogoutController
from .get_all_comments import GetAllCommentsController
