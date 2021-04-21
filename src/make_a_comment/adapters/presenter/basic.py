from functools import wraps

from .interface import PresenterInterface
from src.make_a_comment.adapters.response.basic import Response
from src.make_a_comment.adapters.response.type import ResponseType

from src.make_a_comment.adapters.serializer.user import user_serializer

from src.make_a_comment.adapters.response.custom_typing import PositiveResponse

from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from marshmallow import ValidationError
from src.make_a_comment.exceptions.invalid_login_credentials import InvalidLoginCredentials

from src.make_a_comment.exceptions.access_token_required import AccessTokenRequired
from jwt.exceptions import DecodeError, InvalidSignatureError, ExpiredSignatureError, InvalidTokenError


class Presenter(PresenterInterface):

    def __init__(self, serializer):
        self.serializer = serializer

    def build_response(self, function, positive_response: PositiveResponse = ResponseType.SUCCESS):
        @wraps(function)
        def wrapper(*args, **kwargs):

            # payload = user_serializer.dump()

            # aqui eu tenho que fazer a validação dos dados de entrada

            try:
                "INPUT VALIDATION"
            except ValidationError as error:
                # file_logger.info(error.messages, extra=extra_loggin)
                # traceback.print_exc()
                return Response.bad_request(error)

            try:
                payload = function(*args, **kwargs)
                payload = self.serializer.dump(payload)
            except NoResultFound as error:
                # file_logger.info(error.orig, extra=extra_loggin)
                # traceback.print_exc()
                return Response.not_found(error)
            except IntegrityError as error:
                # file_logger.info(error.orig, extra=extra_loggin)
                # traceback.print_exc()
                return Response.bad_request(error)
            except SQLAlchemyError as error:
                # file_logger.error(str(error), extra=extra_loggin)
                # traceback.print_exc()
                return Response.internal_server_error(error)
            except AccessTokenRequired as error:
                # file_logger.error(str(error), extra=extra_loggin)
                # traceback.print_exc()
                return Response.bad_request(error)
            except InvalidTokenError as error:
                # file_logger.error(str(error), extra=extra_loggin)
                # traceback.print_exc()
                return Response.unauthorized(error)
            except DecodeError as error:
                # file_logger.error(str(error), extra=extra_loggin)
                # traceback.print_exc()
                return Response.unauthorized(error)
            except InvalidSignatureError as error:
                # file_logger.error(str(error), extra=extra_loggin)
                # traceback.print_exc()
                return Response.unauthorized(error)
            except ExpiredSignatureError as error:
                # file_logger.error(str(error), extra=extra_loggin)
                # traceback.print_exc()
                return Response.unauthorized(error)
            # except InvalidLoginCredentials as error:
            #     file_logger.error(str(error), extra=extra_loggin)
            #     traceback.print_exc()
            #     return Response.bad_request(error)

            except Exception as error:
                # file_logger.error(str(error), extra=extra_loggin)
                # traceback.print_exc()
                return Response.internal_server_error(error)

            return Response(
                kind=positive_response,
                payload=payload,
                message="success")

        return wrapper
