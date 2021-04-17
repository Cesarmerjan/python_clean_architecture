from pprint import pprint
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def get_a_user_by_uuid(options):
    user_uow = UserUoW(options.session_factory)

    request_json = {"user_uuid": options.user_uuid}

    user = controller.get_a_user_by_uuid(request_json=request_json,
                                         user_uow=user_uow)

    pprint(user)
