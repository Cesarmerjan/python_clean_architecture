from flask import request, jsonify, current_app
from src.make_a_comment.adapters.response.status_code import STATUS_CODE
from src.make_a_comment.adapters.controller.factory import ControllerFactory


def get_a_user_by_uuid(user_uuid):
    request_json = request.get_json()
    request_json = {} if not request_json else request_json

    request_json["user_uuid"] = user_uuid

    controller = ControllerFactory("get_user_by_uuid",
                                   current_app.session_factory)

    response = controller.handle(request_json)

    return jsonify(response.payload), STATUS_CODE[response.kind]
