from .view_all_comments import view_all_comments
from .get_a_comment_by_uuid import get_a_comment_by_uuid
from .delete_a_comment_by_uuid import delete_a_comment_by_uuid
from .update_a_comment import update_a_comment


def register_comment_resources(bp):
    bp.add_url_rule(rule="/view_all_comments",
                    endpoint="view_all_comments",
                    view_func=view_all_comments,
                    methods=["GET"])

    bp.add_url_rule(rule="/get_a_comment_by_uuid/<string:comment_uuid>",
                    endpoint="get_a_comment_by_uuid",
                    view_func=get_a_comment_by_uuid,
                    methods=["GET"])

    bp.add_url_rule(rule="/delete_a_comment_by_uuid/<string:comment_uuid>",
                    endpoint="delete_a_comment_by_uuid",
                    view_func=delete_a_comment_by_uuid,
                    methods=["DELETE"])

    bp.add_url_rule(rule="/update_a_comment",
                    endpoint="update_a_comment",
                    view_func=update_a_comment,
                    methods=["POST"])
