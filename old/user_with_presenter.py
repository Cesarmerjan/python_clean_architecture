from copy import deepcopy
from functools import wraps

from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment

from werkzeug.security import check_password_hash
from src.make_a_comment.utils.jwt_handler import generate_access_token
from src.make_a_comment.utils.jwt_handler import ACCESS_TOKEN_BLACKLIST

from src.make_a_comment.exceptions.invalid_login_credentials import InvalidLoginCredentials

from .user_interface import UserServiceInterface
from src.make_a_comment.adapters.presenter.interface import PresenterInterface
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from src.make_a_comment.adapters.response.type import ResponseType
from src.make_a_comment.adapters.response.basic import Response

from src.make_a_comment.adapters.response.custom_typing import PositiveResponse

from .login_required import login_required


class UserService(UserServiceInterface):

    def __init__(self, user_uow: UoWInterface, presenter: PresenterInterface):
        self.uow = user_uow
        self.presenter = presenter

    def build_response(positive_response: PositiveResponse):
        def inner_function(function):
            @wraps(function)
            def wrapper(self, *args, **kwargs):
                response = self.presenter.build_response(
                    function,
                    positive_response
                )(self, *args, **kwargs)
                return response
            return wrapper
        return inner_function

    @build_response(ResponseType.CREATED)
    def register_user(self, *args, **kwargs) -> Response:
        return self._register_user(*args, **kwargs)
        # response = self.presenter.build_response(
        #     self._register_user, ResponseType.CREATED)(*args, **kwargs)
        # return response

    def _register_user(self, name: str, email: str, password: str, admin: bool = None) -> User:
        with self.uow:
            user = self.uow.repository.add(
                User(name, email, password, admin)
            )
            user_copy = deepcopy(user)
            self.uow.commit()
        return user_copy

    def get_user_by_uuid(self, *args, **kwargs) -> Response:
        response = self.presenter.build_response(
            self._get_user_by_uuid, ResponseType.SUCCESS)(*args, **kwargs)
        return response

    def _get_user_by_uuid(self, user_uuid: "User.uuid") -> User:
        with self.uow:
            user = self.uow.repository.get_by(uuid=user_uuid)
            # This (user.comments) needs to be here because of the relationship
            # This query all comments of the user before creating the deepcopy
            # If this is not here you will get the following error:
            # sqlalchemy.orm.exc.DetachedInstanceError
            user.comments
            user_copy = deepcopy(user)
        return user_copy

    @login_required
    def make_a_comment(self, access_token, *args, **kwargs) -> Response:
        response = self.presenter.build_response(
            self._make_a_comment,
            ResponseType.CREATED)(*args, **kwargs)
        return response

    def _make_a_comment(self, user_uuid: "User.uuid", text: str) -> Comment:
        with self.uow:
            user = self.uow.repository.get_by(uuid=user_uuid)
            comment = Comment(text)
            comment_copy = deepcopy(comment)
            user.make_a_comment(comment)
            self.uow.repository.add(user)
            self.uow.commit()
        return comment_copy

    def login(self, *args, **kwargs) -> Response:
        response = self.presenter.build_response(
            self._login, ResponseType.SUCCESS)(*args, **kwargs)
        return response

    def _login(self, email: "User.email", password: str) -> dict:
        with self.uow:
            user = self.uow.repository.get_by(email=email)

            if not self.verify_user_password(user.password_hash, password):
                raise InvalidLoginCredentials

            payload = {"user_uuid": user.uuid}

            access_token = generate_access_token(payload)

        return {"access_token": access_token}

    @login_required
    def logout(self, access_token, *args, **kwargs) -> Response:
        response = self.presenter.build_response(
            self._logout, ResponseType.SUCCESS)(access_token)
        return response

    def _logout(self, access_token: str) -> None:
        ACCESS_TOKEN_BLACKLIST.add(access_token)

    @staticmethod
    def verify_user_password(user_password_hash: "User.password_hash", password: str) -> bool:
        return check_password_hash(user_password_hash, password)
