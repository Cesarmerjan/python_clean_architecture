import traceback
from src.make_a_comment.adapters.output.basic import BasicOutput
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface
from src.make_a_comment.serializer.user import user_serializer

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.make_a_comment.utils.logging_handler import file_logger

from src.make_a_comment.use_case import service

from src.make_a_comment.adapters.input.user.create import CreateUserInput


def create_a_user(data: dict, user_uow: UoWInterface) -> BasicOutput:

    extra_loggin = {"function": "create_a_user"}

    try:
        user_input = CreateUserInput(data)
        parsed_input = user_input.to_dict()
        # parsed_request = user_serializer.load(data)
    except ValidationError as error:
        file_logger.info(error.messages, extra=extra_loggin)
        traceback.print_exc()
        return BasicOutput(400, error)

    try:
        user = service.create_a_user(**parsed_input, user_uow=user_uow)
    except IntegrityError as error:
        file_logger.info(error.orig, extra=extra_loggin)
        traceback.print_exc()
        return BasicOutput(400, error)
    except SQLAlchemyError as error:
        file_logger.error(str(error), extra=extra_loggin)
        traceback.print_exc()
        return BasicOutput(500, error)

    try:
        response_data = user_serializer.dump(user)
        return BasicOutput(201, "OK", response_data)
    except Exception as error:
        file_logger.error(str(error), extra=extra_loggin)
        traceback.print_exc()
        return BasicOutput(500, error)
