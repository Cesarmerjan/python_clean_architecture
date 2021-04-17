from flask import request, jsonify, current_app
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW


def view_all_comments():

    comment_uow = CommentUoW(current_app.session_factory)

    comments = controller.view_all_comments(comment_uow=comment_uow)

    return jsonify(comments), 200
