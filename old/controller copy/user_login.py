import traceback
from src.make_a_comment.adapters.output.basic import BasicOutput
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from src.make_a_comment.adapters.serializer.user import user_serializer

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from src.make_a_comment.exceptions.invalid_login_credentials import InvalidLoginCredentials
from src.make_a_comment.exceptions.missing_data_on_request import MissingUserEmail, MissingUserPassword

from src.make_a_comment.utils.logging_handler import file_logger

from src.make_a_comment.use_case import service

from src.make_a_comment.adapters.input.user.login import LoginUserInput


def user_login(data, user_uow: UoWInterface) -> BasicOutput:

    # Criar a resposta com o cabeçalho setando os hhtponly cookies ao invez de setar eles com o flask

    extra_loggin = {"function": "user_login"}

    # user_email = data.get("email")
    # if not user_email:
    #     raise MissingUserEmail

    try:
        # parsed_email = user_serializer.declared_fields.get(
        #     "email").deserialize(user_email)
        user_login_input = LoginUserInput(data)
        parsed_input = user_login_input.to_dict()
    except ValidationError as error:
        traceback.print_exc()
        raise error  # error.messages

    # user_password = data.get("password")
    # if not user_password:
    #     raise MissingUserPassword

    # try:
    #     parsed_password = user_serializer.declared_fields.get(
    #         "password").deserialize(user_password)
    # except ValidationError as error:
    #     traceback.print_exc()
    #     raise error  # error.messages

    try:
        access_token = service.user_login(**parsed_input,
                                          user_uow=user_uow)
        # access_token = service.user_login(email=user_email,
        #                                   password=user_password,
        #                                   user_uow=user_uow)
    except NoResultFound as error:
        traceback.print_exc()
        raise error
    except SQLAlchemyError as error:
        traceback.print_exc()
        raise error
    except InvalidLoginCredentials as error:
        traceback.print_exc()
        raise error

    return access_token
