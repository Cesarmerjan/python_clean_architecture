from pprint import pprint
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def register_user(options):
    request_json = {"name": options.name,
                    "email": options.email,
                    "password": options.password}

    user_uow = UserUoW(options.session_factory)

    response = controller.create_a_user(request_json,
                                        user_uow=user_uow)

    pprint(response)
