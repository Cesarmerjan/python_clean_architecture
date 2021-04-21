from flask import request, jsonify, current_app
from src.make_a_comment.adapters.response.status_code import STATUS_CODE
from src.make_a_comment.adapters.controller.factory import ControllerFactory
from src.make_a_comment.utils.jwt_handler import get_jwt_payload


def make_a_comment():
    request_json = request.get_json()
    request_json = {} if not request_json else request_json

    access_token = request.cookies.get("access_token")

    request_json["access_token"] = access_token

    if access_token:
        user_uuid = get_jwt_payload(access_token)["user_uuid"]
    else:
        user_uuid = None

    request_json["user_uuid"] = user_uuid

    controller = ControllerFactory("maka_a_comment",
                                   current_app.session_factory)

    response = controller.handle(request_json)

    return jsonify(response.payload), STATUS_CODE[response.kind]
