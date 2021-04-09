from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.user_uow import UserUoW


def make_a_comment(options):
    access_token = options.access_token

    request_json = {"text": options.text}

    user_uow = UserUoW(options.session_factory)

    response = interactor.make_a_user_comment(request_json,
                                              user_uow=user_uow,
                                              access_token=access_token)

    print(response)
