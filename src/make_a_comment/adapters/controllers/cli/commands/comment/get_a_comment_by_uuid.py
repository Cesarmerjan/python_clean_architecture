from src.make_a_comment.use_case import interactor
from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW


def get_a_comment_by_uuid(options):
    comment_uow = CommentUoW(options.session_factory)

    request_json = {"comment_uuid": options.comment_uuid}

    comment = interactor.get_a_comment_by_uuid(request_json=request_json,
                                               comment_uow=comment_uow)

    print(comment)
