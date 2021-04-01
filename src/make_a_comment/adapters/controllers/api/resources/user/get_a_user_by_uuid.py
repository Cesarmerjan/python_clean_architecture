from flask import request, jsonify, current_app
from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def get_a_user_by_uuid(user_uuid):
    user_uow = UserUoW(current_app.session_factory)

    request_json = {"user_uuid": user_uuid}

    user = interactor.get_a_user_by_uuid(request_json=request_json,
                                         user_uow=user_uow)

    return jsonify(user), 200
