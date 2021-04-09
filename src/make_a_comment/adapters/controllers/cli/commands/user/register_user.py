from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def register_user(options):
    request_json = {"name": options.name,
                    "email": options.email,
                    "password": options.password}

    user_uow = UserUoW(options.session_factory)

    response = interactor.create_a_user(request_json,
                                        user_uow=user_uow)

    print(response)
