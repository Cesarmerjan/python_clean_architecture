from pprint import pprint
from src.make_a_comment.adapters import controller
from src.make_a_comment.adapters.unit_of_work.comment_uow import CommentUoW


def update_a_comment(options):
    access_token = options.access_token

    request_json = {"comment_uuid": options.comment_uuid,
                    "new_text": options.new_text}

    comment_uow = CommentUoW(options.session_factory)

    comment = controller.update_a_comment(request_json=request_json,
                                          comment_uow=comment_uow,
                                          access_token=access_token)

    pprint(comment)
