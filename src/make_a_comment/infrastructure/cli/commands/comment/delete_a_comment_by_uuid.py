from pprint import pprint
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW


def delete_a_comment_by_uuid(options):
    access_token = options.access_token

    comment_uow = CommentUoW(options.session_factory)

    request_json = {"comment_uuid": options.comment_uuid}

    controller.delete_a_comment_by_uuid(request_json=request_json,
                                        comment_uow=comment_uow,
                                        access_token=access_token)

    pprint("OK")
