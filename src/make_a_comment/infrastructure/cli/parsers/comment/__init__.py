from .view_all_comments import register_view_all_comments_parser
from .delete_a_comment_by_uuid import register_delete_a_comment_by_uuid_parser
from .get_a_comment_by_uuid import register_get_a_comment_by_uuid_parser
from .update_a_comment import register_update_a_comment_parser


def register_comment_parsers(subparsers):
    register_view_all_comments_parser(subparsers)
    register_delete_a_comment_by_uuid_parser(subparsers)
    register_get_a_comment_by_uuid_parser(subparsers)
    register_update_a_comment_parser(subparsers)
