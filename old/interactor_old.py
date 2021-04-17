# """Responsible for managing interaction with the business rules (service). Parse the request and build the response"""
# import traceback
# import logging
# import logging.config
# from typing import List
# import functools

# from src.make_a_comment.utils.jwt_handler import ACCESS_TOKEN_BLACKLIST, validate_access_token

# from src.make_a_comment.domain.user import User
# from src.make_a_comment.serializer.user import user_serializer
# from src.make_a_comment.domain.comment import Comment
# from src.make_a_comment.serializer.comment import comment_serializer
# from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

# from . import service

# from src.make_a_comment.request.comment_parser import CommentRequestParser
# from src.make_a_comment.request.user_parser import UserRequestParser
# from src.make_a_comment.adapters.output.basic import BasicOutput

# from marshmallow import ValidationError
# from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
# from jwt.exceptions import DecodeError, InvalidSignatureError, ExpiredSignatureError, InvalidTokenError
# from src.make_a_comment.exceptions.access_token_required import AccessTokenRequired
# from src.make_a_comment.exceptions.invalid_login_credentials import InvalidLoginCredentials
# from src.make_a_comment.exceptions.user_uuid_is_not_in_the_access_token_payload import UserUuidIsNotInAccessTokenPayload
# from src.make_a_comment.exceptions.missing_data_on_request import (
#     MissingCommentUuid,
#     MissingNewCommentText,
#     MissingUserUuid,
#     MissingUserEmail,
#     MissingUserPassword)

# Dentro de cada metodo vou contruir a resposta usando o objeto de resposta enviado pelo controle
# em cada try block vou adicionar o erro na resposta e devolver a resposta
# aqui eu implemento a interface de resposta
# Devo colocar um if para caso a consulta do get by seja None

# logging.config.fileConfig("src/logging.conf")

# file_logger = logging.getLogger("file_logger")


# def login_required(func):
#     @ functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         access_token = kwargs.get("access_token")

#         if not access_token:
#             args_access_token_index = inspect.getfullargspec(
#                 func).args.index("access_token")

#             if not args_access_token_index >= len(args):
#                 access_token = args[args_access_token_index]

#         if not access_token:
#             raise AccessTokenRequired

#         if access_token in ACCESS_TOKEN_BLACKLIST:
#             raise InvalidTokenError

#         try:
#             validate_access_token(access_token)
#         except jwt.exceptions.InvalidSignatureError as error:
#             raise error
#         except jwt.exceptions.ExpiredSignatureError as error:
#             raise error
#         except jwt.exceptions.DecodeError as error:
#             raise error

#         return func(*args, **kwargs)

#     return wrapper


# def create_a_user(data: dict, user_uow: UoWInterface) -> User:

#     extra_loggin = {"function": "create_a_user"}

#     # parser = UserRequestParser(data)

#     # if not parser.request_data_is_valid:
#     #     file_logger.info(parser.request_exceptions_messages,
#     #                      extra=extra_loggin)
#     #     return BasicOutput(400, parser.request_exceptions_messages)

#     try:
#         parsed_request = user_serializer.load(data)
#     except ValidationError as error:
#         file_logger.info(error.messages, extra=extra_loggin)
#         traceback.print_exc()
#         return BasicOutput(400, error)

#     try:
#         user = service.create_a_user(**parsed_request, user_uow=user_uow)
#     except IntegrityError as error:
#         file_logger.info(error.orig, extra=extra_loggin)
#         traceback.print_exc()
#         return BasicOutput(400, error)
#     except SQLAlchemyError as error:
#         file_logger.error(str(error), extra=extra_loggin)
#         traceback.print_exc()
#         return BasicOutput(500, error)

#     try:
#         response_data = user_serializer.dump(user)
#         return BasicOutput(201, "OK", response_data)
#     except Exception as error:
#         file_logger.error(str(error), extra=extra_loggin)
#         traceback.print_exc()
#         return BasicOutput(500, error)

#     # try:
#     #     parsed_request = user_serializer.load(data)
#     # except ValidationError as error:
#     #     file_logger.info(error.messages, extra=extra_loggin)
#     #     traceback.print_exc()
#     #     raise error

#     # try:
#     #     user = service.create_a_user(**parsed_request, user_uow=user_uow)
#     # except IntegrityError as error:
#     #     file_logger.info(error.orig, extra=extra_loggin)
#     #     traceback.print_exc()
#     #     raise error
#     # except SQLAlchemyError as error:
#     #     file_logger.error(str(error), extra=extra_loggin)
#     #     traceback.print_exc()
#     #     raise error
#     # try:
#     #     response = user_serializer.dump(user)
#     # except Exception as error:
#     #     file_logger.critical(str(error), extra=extra_loggin)
#     #     traceback.print_exc()
#     #     raise error

#     # return response


# @ login_required
# def make_a_user_comment(data: dict, user_uow: UoWInterface, access_token: str) -> Comment:
#     extra_loggin = {"function": "make_a_user_comment"}

#     try:
#         access_token_payload = get_payload_from_jwt(access_token)
#     except DecodeError as error:
#         print(error)
#         traceback.print_exc()
#         raise error

#     user_uuid = access_token_payload.get("user_uuid")

#     if not user_uuid:
#         raise UserUuidIsNotInAccessTokenPayload

#     try:
#         parsed_request = comment_serializer.load(data)
#     except ValidationError as error:
#         traceback.print_exc()
#         raise error  # error.messages

#     try:
#         comment = service.make_a_user_comment(**parsed_request,
#                                               user_uuid=user_uuid,
#                                               user_uow=user_uow)
#     except NoResultFound as error:
#         traceback.print_exc()
#         raise error
#     except SQLAlchemyError as error:
#         traceback.print_exc()
#         raise error

#     try:
#         response = comment_serializer.dump(comment)
#     except Exception as error:
#         traceback.print_exc()
#         raise error

#     return response


# def get_a_comment_by_uuid(data: dict, comment_uow: UoWInterface) -> Comment:

#     extra_loggin = {"function": "get_a_comment_by_uuid"}

#     comment_uuid = data.get("comment_uuid")
#     if not comment_uuid:
#         raise MissingCommentUuid

#     try:
#         parsed_uuid = comment_serializer.declared_fields.get(
#             "uuid").deserialize(comment_uuid)
#     except ValidationError as error:
#         traceback.print_exc()
#         raise error  # error.messages

#     try:
#         comment = service.get_a_comment_by_uuid(
#             parsed_uuid, comment_uow=comment_uow)
#     except NoResultFound as error:
#         traceback.print_exc()
#         raise error
#     except SQLAlchemyError as error:
#         traceback.print_exc()
#         raise error

#     try:
#         response = comment_serializer.dump(comment)
#     except Exception as error:
#         traceback.print_exc()
#         raise error

#     return response


# @login_required
# def delete_a_comment_by_uuid(data: dict, comment_uow: UoWInterface, access_token: str) -> None:

#     extra_loggin = {"function": "delete_a_comment_by_uuid"}

#     comment_uuid = data.get("comment_uuid")
#     if not comment_uuid:
#         raise MissingCommentUuid

#     try:
#         parsed_uuid = comment_serializer.declared_fields.get(
#             "uuid").deserialize(comment_uuid)
#     except ValidationError as error:
#         traceback.print_exc()
#         raise error  # error.messages

#     try:
#         comment = service.delete_a_comment_by_uuid(
#             parsed_uuid, comment_uow=comment_uow)
#     except NoResultFound as error:
#         traceback.print_exc()
#         raise error
#     except SQLAlchemyError as error:
#         traceback.print_exc()
#         raise error


# @login_required
# def update_a_comment(data: dict, comment_uow: UoWInterface, access_token: str) -> Comment:

#     extra_loggin = {"function": "update_a_comment"}

#     comment_uuid = data.get("comment_uuid")
#     if not comment_uuid:
#         raise MissingCommentUuid

#     try:
#         parsed_uuid = comment_serializer.declared_fields.get(
#             "uuid").deserialize(comment_uuid)
#     except ValidationError as error:
#         traceback.print_exc()
#         raise error  # error.messages

#     new_text = data.get("new_text")

#     if not new_text:
#         raise MissingNewCommentText

#     try:
#         parsed_new_text = comment_serializer.declared_fields.get(
#             "text").deserialize(new_text)
#     except ValidationError as error:
#         traceback.print_exc()
#         raise error  # error.messages

#     try:
#         comment = service.update_a_comment(
#             parsed_uuid, parsed_new_text, comment_uow)
#     except NoResultFound as error:
#         traceback.print_exc()
#         raise error
#     except SQLAlchemyError as error:
#         traceback.print_exc()
#         raise error

#     try:
#         response = comment_serializer.dump(comment)
#     except Exception as error:
#         traceback.print_exc()
#         raise error

#     return response


# def get_a_user_by_uuid(data: dict, user_uow: UoWInterface):

#     extra_loggin = {"function": "get_a_user_by_uuid"}

#     user_uuid = data.get("user_uuid")
#     if not user_uuid:
#         raise MissingUserUuid

#     try:
#         parsed_uuid = user_serializer.declared_fields.get(
#             "uuid").deserialize(user_uuid)
#     except ValidationError as error:
#         traceback.print_exc()
#         raise error  # error.messages

#     try:
#         user = service.get_a_user_by_uuid(parsed_uuid, user_uow)
#     except NoResultFound as error:
#         traceback.print_exc()
#         raise error
#     except SQLAlchemyError as error:
#         traceback.print_exc()
#         raise error

#     try:
#         response = user_serializer.dump(user)
#     except Exception as error:
#         traceback.print_exc()
#         raise error

#     return response


# def view_all_comments(comment_uow: UoWInterface) -> List[Comment]:

#     extra_loggin = {"function": "view_all_comments"}

#     comments = service.view_all_comments(comment_uow)

#     try:
#         response = comment_serializer.dump(comments, many=True)
#     except Exception as error:
#         traceback.print_exc()
#         raise error

#     return response


# def user_login(data, user_uow: UoWInterface) -> str:

#     # Criar a resposta com o cabeçalho setando os hhtponly cookies ao invez de setar eles com o flask

#     extra_loggin = {"function": "user_login"}

#     user_email = data.get("email")
#     if not user_email:
#         raise MissingUserEmail

#     try:
#         parsed_email = user_serializer.declared_fields.get(
#             "email").deserialize(user_email)
#     except ValidationError as error:
#         traceback.print_exc()
#         raise error  # error.messages

#     user_password = data.get("password")
#     if not user_password:
#         raise MissingUserPassword

#     try:
#         parsed_password = user_serializer.declared_fields.get(
#             "password").deserialize(user_password)
#     except ValidationError as error:
#         traceback.print_exc()
#         raise error  # error.messages

#     try:
#         access_token = service.user_login(email=user_email,
#                                           password=user_password,
#                                           user_uow=user_uow)
#     except NoResultFound as error:
#         traceback.print_exc()
#         raise error
#     except SQLAlchemyError as error:
#         traceback.print_exc()
#         raise error
#     except InvalidLoginCredentials as error:
#         traceback.print_exc()
#         raise error

#     return access_token


# @login_required
# def user_logout(access_token):
#     return service.user_logout(access_token)


# def verify_access_token(access_token):

#     extra_loggin = {"function": "verify_access_token"}

#     try:
#         return service.verify_access_token(access_token)
#     except DecodeError as error:
#         traceback.print_exc()
#         raise error  # bad formated access token
#     except InvalidSignatureError as error:
#         traceback.print_exc()
#         raise error  # bad signature
#     except ExpiredSignatureError as error:
#         traceback.print_exc()
#         raise error  # expired token
#     except InvalidTokenError as error:
#         traceback.print_exc()
#         raise error  # token after loged out


# def verify_user_password(user_password_hash: "User.password_hash", password: str) -> bool:
#     return service.verify_user_password(user_password_hash, password)


# def get_jwt_identity(access_token):

#     extra_loggin = {"function": "get_jwt_identity"}

#     try:
#         return service.get_jwt_identity(access_token)
#         traceback.print_exc()
#     except DecodeError as error:
#         traceback.print_exc()
#         # raise error  # bad formated access token


# def get_payload_from_jwt(access_token):

#     extra_loggin = {"function": "get_payload_from_jwt"}

#     try:
#         return service.get_payload_from_jwt(access_token)
#         traceback.print_exc()
#     except DecodeError as error:
#         traceback.print_exc()
#         # raise error  # bad formated access token
