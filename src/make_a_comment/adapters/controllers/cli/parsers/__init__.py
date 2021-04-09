from .user import register_user_parsers
from .comment import register_comment_parsers


def register_parsers(subparsers):
    register_user_parsers(subparsers)
    register_comment_parsers(subparsers)
