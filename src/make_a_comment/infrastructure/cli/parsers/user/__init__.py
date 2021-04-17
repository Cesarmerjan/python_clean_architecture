from .register_user import register_register_user_parser
from .login import register_login_parser
from .logout import register_logout_parser
from .get_a_user_by_uuid import register_get_a_user_by_uuid_parser
from .make_a_comment import register_make_a_comment_parser


def register_user_parsers(subparsers):
    register_register_user_parser(subparsers)
    register_login_parser(subparsers)
    register_logout_parser(subparsers)
    register_get_a_user_by_uuid_parser(subparsers)
    register_make_a_comment_parser(subparsers)
