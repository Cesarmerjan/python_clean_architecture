import traceback
from src.make_a_comment.adapters.output.basic import BasicOutput
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from src.make_a_comment.adapters.serializer.comment import comment_serializer

from src.make_a_comment.exceptions.user_uuid_is_not_in_the_access_token_payload import UserUuidIsNotInAccessTokenPayload
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from src.make_a_comment.utils.logging_handler import file_logger

from src.make_a_comment.utils.jwt_handler import get_jwt_payload

from .login_required import login_required

from src.make_a_comment.use_case import service

from src.make_a_comment.adapters.input.user.create import CreateUserInput


@login_required
def make_a_user_comment(data: dict, user_uow: UoWInterface, access_token: str) -> BasicOutput:
    extra_loggin = {"function": "make_a_user_comment"}

    try:
        access_token_payload = get_jwt_payload(access_token)
    except DecodeError as error:
        traceback.print_exc()
        raise error

    user_uuid = access_token_payload.get("user_uuid")

    if not user_uuid:
        raise UserUuidIsNotInAccessTokenPayload

    try:
        parsed_request = comment_serializer.load(data)
    except ValidationError as error:
        traceback.print_exc()
        raise error

    try:
        comment = service.make_a_user_comment(**parsed_request,
                                              user_uuid=user_uuid,
                                              user_uow=user_uow)
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
