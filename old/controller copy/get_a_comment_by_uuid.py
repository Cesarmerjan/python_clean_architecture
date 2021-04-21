import traceback
from src.make_a_comment.adapters.output.basic import BasicOutput
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from src.make_a_comment.adapters.serializer.comment import comment_serializer

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from src.make_a_comment.utils.logging_handler import file_logger

from src.make_a_comment.use_case import service

# from src.make_a_comment.exceptions.missing_data_on_request import MissingCommentUuid

from src.make_a_comment.adapters.input.comment.uuid_only import CommentUuidOnlyInput


def get_a_comment_by_uuid(data: dict, comment_uow: UoWInterface) -> BasicOutput:

    extra_loggin = {"function": "get_a_comment_by_uuid"}

    # comment_uuid = data.get("comment_uuid")
    # if not comment_uuid:
    #     raise MissingCommentUuid

    try:
        # parsed_uuid = comment_serializer.declared_fields.get(
        #     "uuid").deserialize(comment_uuid)
        comment_uuid_input = CommentUuidOnlyInput(data)
        parsed_input = comment_uuid_input.to_dict()
    except ValidationError as error:
        traceback.print_exc()
        raise error  # error.messages

    try:
        comment = service.get_a_comment_by_uuid(
            **parsed_input, comment_uow=comment_uow)
        # comment = service.get_a_comment_by_uuid(
        #     parsed_uuid, comment_uow=comment_uow)
    except NoResultFound as error:
        traceback.print_exc()
        raise error
    except SQLAlchemyError as error:
        traceback.print_exc()
        raise error

    try:
        response = comment_serializer.dump(comment)
    except Exception as error:
        traceback.print_exc()
        raise error

    return response
