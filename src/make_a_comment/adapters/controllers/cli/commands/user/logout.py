from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def logout(options):
    access_token = options.access_token

    interactor.user_logout(access_token=access_token)

    print(200)
