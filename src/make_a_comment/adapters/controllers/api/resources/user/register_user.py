from flask import request, jsonify, current_app
from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def register_user():
    request_json = request.get_json()

    user_uow = UserUoW(current_app.session_factory)

    response = interactor.create_a_user(request_json,
                                        user_uow=user_uow)

    return jsonify(response), 201
