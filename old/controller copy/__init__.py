"""Responsible for managing interaction with the business rules (service). Parse the request and build the response"""
from .create_a_user import create_a_user
from .make_a_user_comment import make_a_user_comment
from .get_a_comment_by_uuid import get_a_comment_by_uuid
from .delete_a_comment_by_uuid import delete_a_comment_by_uuid
from .update_a_comment import update_a_comment
from .get_a_user_by_uuid import get_a_user_by_uuid
from .view_all_comments import view_all_comments
from .user_login import user_login
from .user_logout import user_logout
