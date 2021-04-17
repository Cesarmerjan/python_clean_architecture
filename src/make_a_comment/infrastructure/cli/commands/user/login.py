from pprint import pprint
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def login(options):
    request_json = {"email": options.email,
                    "password": options.password}

    user_uow = UserUoW(options.session_factory)

    access_token = controller.user_login(request_json,
                                         user_uow=user_uow)

    pprint(access_token)
