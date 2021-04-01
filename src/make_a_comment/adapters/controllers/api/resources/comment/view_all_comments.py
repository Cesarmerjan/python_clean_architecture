from flask import request, jsonify, current_app
from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW


def view_all_comments():

    comment_uow = CommentUoW(current_app.session_factory)

    comments = interactor.view_all_comments(comment_uow=comment_uow)

    return jsonify(comments), 200
