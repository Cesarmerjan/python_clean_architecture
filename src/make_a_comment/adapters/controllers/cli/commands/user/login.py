from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def login(options):
    request_json = {"email": options.email,
                    "password": options.password}

    user_uow = UserUoW(options.session_factory)

    access_token = interactor.user_login(request_json,
                                         user_uow=user_uow)

    print(access_token)
