from flask import request, jsonify, current_app
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def register_user():
    request_json = request.get_json()

    user_uow = UserUoW(current_app.session_factory)

    response = controller.create_a_user(request_json,
                                        user_uow=user_uow)

    if response.data:
        return jsonify(response.data), response.http_status_code
    else:
        return response.message, response.http_status_code
