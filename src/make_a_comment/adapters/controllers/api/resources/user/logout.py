from flask import request, jsonify, make_response
from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def logout():
    access_token = request.cookies.get("access_token")

    interactor.user_logout(access_token=access_token)

    response = make_response("ok")
    response.set_cookie(key="access_token",
                        value="",
                        httponly=True,
                        max_age=0,
                        expires=0)

    return response, 200
