import traceback
from src.make_a_comment.adapters.output.basic import BasicOutput
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from src.make_a_comment.adapters.serializer.comment import comment_serializer

from src.make_a_comment.exceptions.missing_data_on_request import MissingCommentUuid, MissingNewCommentText
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from src.make_a_comment.utils.logging_handler import file_logger

from .login_required import login_required

from src.make_a_comment.use_case import service

from src.make_a_comment.adapters.input.comment.update import UpdateCommentInput


# @login_required
def update_a_comment(data: dict, comment_uow: UoWInterface, access_token: str) -> BasicOutput:

    extra_loggin = {"function": "update_a_comment"}

    data["access_token"] = access_token

    # comment_uuid = data.get("comment_uuid")
    # if not comment_uuid:
    #     raise MissingCommentUuid

    try:
        # parsed_uuid = comment_serializer.declared_fields.get(
        #     "uuid").deserialize(comment_uuid)
        comment_input = UpdateCommentInput(data)
        parsed_input = comment_input.to_dict()
    except ValidationError as error:
        traceback.print_exc()
        raise error  # error.messages
    except jwt.exceptions.InvalidSignatureError as error:
        raise error
    except jwt.exceptions.ExpiredSignatureError as error:
        raise error
    except jwt.exceptions.DecodeError as error:
        raise error
    except AccessTokenRequired as error:
        raise error

    # new_text = data.get("new_text")

    # if not new_text:
    #     raise MissingNewCommentText

    # try:
    #     parsed_new_text = comment_serializer.declared_fields.get(
    #         "text").deserialize(new_text)
    # except ValidationError as error:
    #     traceback.print_exc()
    #     raise error  # error.messages

    try:
        comment = service.update_a_comment(
            **parsed_input, comment_uow=comment_uow)
        # comment = service.update_a_comment(
        #     parsed_uuid, parsed_new_text, comment_uow)
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
