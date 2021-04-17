from pprint import pprint
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def logout(options):
    access_token = options.access_token

    controller.user_logout(access_token=access_token)

    pprint(200)
