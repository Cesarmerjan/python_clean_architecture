from .register_user import register_user
from .login import login
from .logout import logout
from .make_a_comment import make_a_comment
from .get_a_user_by_uuid import get_a_user_by_uuid


def register_user_resources(bp):
    bp.add_url_rule(rule="/register_user",
                    endpoint="register_user",
                    view_func=register_user,
                    methods=["POST"])

    bp.add_url_rule(rule="/login",
                    endpoint="login",
                    view_func=login,
                    methods=["POST"])

    bp.add_url_rule(rule="/logout",
                    endpoint="logout",
                    view_func=logout,
                    methods=["GET"])

    bp.add_url_rule(rule="/make_a_comment",
                    endpoint="make_a_comment",
                    view_func=make_a_comment,
                    methods=["POST"])

    bp.add_url_rule(rule="/get_a_user_by_uuid/<string:user_uuid>",
                    endpoint="get_a_user_by_uuid",
                    view_func=get_a_user_by_uuid,
                    methods=["GET"])
