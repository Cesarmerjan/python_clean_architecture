from flask import request, jsonify, current_app
from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW


def update_a_comment():
    access_token = request.cookies.get("access_token")

    request_json = request.get_json()

    comment_uow = CommentUoW(current_app.session_factory)

    comment = interactor.update_a_comment(request_json=request_json,
                                          comment_uow=comment_uow,
                                          access_token=access_token)

    return jsonify(comment), 200
