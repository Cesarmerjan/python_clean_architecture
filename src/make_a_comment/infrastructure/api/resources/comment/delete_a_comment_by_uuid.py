from flask import request, jsonify, current_app
from src.make_a_comment.adapters.response.status_code import STATUS_CODE
from src.make_a_comment.adapters.controller.factory import ControllerFactory
from src.make_a_comment.utils.jwt_handler import get_jwt_payload


def delete_a_comment_by_uuid(comment_uuid):
    request_json = request.get_json()
    request_json = {} if not request_json else request_json

    access_token = request.cookies.get("access_token")

    request_json["access_token"] = access_token

    request_json["comment_uuid"] = comment_uuid

    controller = ControllerFactory("update_a_comment",
                                   current_app.session_factory)

    response = controller.handle(request_json)

    return jsonify(response.payload), STATUS_CODE[response.kind]
