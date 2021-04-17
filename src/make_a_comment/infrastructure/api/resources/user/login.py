from flask import request, jsonify, current_app, make_response
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def login():
    request_json = request.get_json()

    user_uow = UserUoW(current_app.session_factory)

    access_token = controller.user_login(request_json,
                                         user_uow=user_uow)

    response = make_response("ok")
    response.set_cookie(key="access_token",
                        value=access_token,
                        httponly=True)

    return response, 200


# bearer = request.headers.get('Authorization')
# token = bearer.split()[1]
