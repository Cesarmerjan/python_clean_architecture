from flask import request, jsonify, current_app, make_response
from src.make_a_comment.adapters.response.status_code import STATUS_CODE
from src.make_a_comment.adapters.controller.factory import ControllerFactory


def login():
    request_json = request.get_json()
    request_json = {} if not request_json else request_json

    controller = ControllerFactory("user_login",
                                   current_app.session_factory)

    response = controller.handle(request_json)

    flask_response = make_response(
        jsonify(response.payload),
        STATUS_CODE[response.kind])

    flask_response.set_cookie(key="access_token",
                              value=response.payload["access_token"],
                              httponly=True)

    return flask_response
