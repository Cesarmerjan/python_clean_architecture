from flask import Blueprint
from .user import register_user_resources
from .comment import register_comment_resources

bp = Blueprint("api", __name__, url_prefix="/api/v0")

register_user_resources(bp)
register_comment_resources(bp)


def register_resources(api):
    api.register_blueprint(bp)
