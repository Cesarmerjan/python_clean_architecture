from flask import request, jsonify, current_app
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW


def delete_a_comment_by_uuid(comment_uuid):
    access_token = request.cookies.get("access_token")

    comment_uow = CommentUoW(current_app.session_factory)

    request_json = {"comment_uuid": comment_uuid}

    controller.delete_a_comment_by_uuid(request_json=request_json,
                                        comment_uow=comment_uow,
                                        access_token=access_token)

    return "Ok", 200
