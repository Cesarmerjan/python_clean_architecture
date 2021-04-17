from flask import request, jsonify, current_app
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def make_a_comment():
    access_token = request.cookies.get("access_token")

    request_json = request.get_json()

    user_uow = UserUoW(current_app.session_factory)

    response = controller.make_a_user_comment(request_json,
                                              user_uow=user_uow,
                                              access_token=access_token)

    return jsonify(response), 201
