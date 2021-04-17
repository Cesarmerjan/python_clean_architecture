import traceback
from src.make_a_comment.adapters.output.basic import BasicOutput
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface
from src.make_a_comment.serializer.user import user_serializer

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.make_a_comment.utils.logging_handler import file_logger

from src.make_a_comment.use_case.service.user_interface import UserServiceInterface

from src.make_a_comment.adapters.input.user.register import RegisterUserInput

# talvez assim eu possa até tirar a palavra controller


class RegisterUser:

    def __init__(self, user_service: UserServiceInterface, presenter: "PresenterInterface"):
        self.user_service = user_service
        self.presenter = presenter

    def __call__(self, request: "RequestObject") -> "ResponseObject":

        extra_loggin = {"function": "create_a_user"}

        # try:
        # parsed_request = self.presenter.parse_request(request)

        try:
            user_input = RegisterUserInput(data)
            parsed_input = user_input.to_dict()
            # parsed_request = user_serializer.load(data)
        except ValidationError as error:
            file_logger.info(error.messages, extra=extra_loggin)
            traceback.print_exc()
            return BasicOutput(400, error)

        # try
            # response = self.user_service.register_user(parsed_request, self.presenter)

        try:
            user = self.user_service.register_user(**parsed_input)
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
