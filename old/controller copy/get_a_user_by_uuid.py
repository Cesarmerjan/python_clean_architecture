import traceback
from src.make_a_comment.adapters.output.basic import BasicOutput
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from src.make_a_comment.adapters.serializer.user import user_serializer

# from src.make_a_comment.exceptions.missing_data_on_request import MissingUserUuid
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from src.make_a_comment.utils.logging_handler import file_logger

from src.make_a_comment.use_case import service

from src.make_a_comment.adapters.input.user.uuid_only import UserUuidOnlyInput


def get_a_user_by_uuid(data: dict, user_uow: UoWInterface) -> BasicOutput:

    extra_loggin = {"function": "get_a_user_by_uuid"}

    # user_uuid = data.get("user_uuid")
    # if not user_uuid:
    #     raise MissingUserUuid

    try:
        user_uuid_input = UserUuidOnlyInput(data)
        # parsed_uuid = user_serializer.declared_fields.get(
        #     "uuid").deserialize(user_uuid)
        parsed_input = user_uuid_input.to_dict()
    except ValidationError as error:
        traceback.print_exc()
        raise error  # error.messages

    try:
        user = service.get_a_user_by_uuid(**parsed_input,
                                          user_uow=user_uow)
        # user = service.get_a_user_by_uuid(parsed_uuid, user_uow)
    except NoResultFound as error:
        traceback.print_exc()
        raise error
    except SQLAlchemyError as error:
        traceback.print_exc()
        raise error

    try:
        response = user_serializer.dump(user)
    except Exception as error:
        traceback.print_exc()
        raise error

    return response
