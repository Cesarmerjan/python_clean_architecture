import traceback
from src.make_a_comment.adapters.output.basic import BasicOutput
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from src.make_a_comment.adapters.serializer.comment import comment_serializer

from sqlalchemy.exc import SQLAlchemyError

from src.make_a_comment.utils.logging_handler import file_logger

from src.make_a_comment.use_case import service


def view_all_comments(comment_uow: UoWInterface) -> BasicOutput:

    extra_loggin = {"function": "view_all_comments"}

    try:
        comments = service.view_all_comments(comment_uow)
    except SQLAlchemyError as error:
        traceback.print_exc()
        raise error

    try:
        response = comment_serializer.dump(comments, many=True)
    except Exception as error:
        traceback.print_exc()
        raise error

    return response
