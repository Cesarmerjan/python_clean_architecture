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


class UserService(UserServiceInterface):

    presenter = None

    def __init__(self, user_uow: UoWInterface, presenter: PresenterInterface = None):
        self.uow = user_uow
        self.presenter = presenter

    def build_response(response_type: ResponseType):
        def inner_function(function):
            @wraps(function)
            def wrapper(self, *args, **kwargs):
                if self.presenter:
                    response = self.presenter.build_response(
                        function,
                        response_type
                    )(self, *args, **kwargs)
                else:
                    response = function(self, *args, **kwargs)
                return response
            return wrapper
        return inner_function

    # create_a_user
    @build_response(ResponseType.CREATED)
    def register_user(self, name: str, email: str, password: str, admin: bool = None) -> User:
        with self.uow:
            user = self.uow.repository.add(
                User(name, email, password, admin)
            )
            user_copy = deepcopy(user)
            self.uow.commit()
        return user_copy

    @build_response
    def get_user_by_uuid(self, user_uuid: "User.uuid") -> User:
        with self.uow:
            user = self.uow.repository.get_by(uuid=user_uuid)
            # This (user.comments) needs to be here because of the relationship
            # This query all comments of the user before creating the deepcopy
            # If this is not here you will get the following error:
            # sqlalchemy.orm.exc.DetachedInstanceError
            user.comments
            user_copy = deepcopy(user)
        return user_copy

    @build_response
    def make_a_comment(self, user_uuid: "User.uuid", text: str) -> Comment:
        with self.uow:
            user = self.uow.repository.get_by(uuid=user_uuid)
            comment = Comment(text)
            comment_copy = deepcopy(comment)
            user.make_a_comment(comment)
            self.uow.repository.add(user)
            self.uow.commit()
        return comment_copy

    @build_response
    def login(self, email: "User.email", password: str) -> "access_token":
        with self.uow:
            user = self.uow.repository.get_by(email=email)

            if not self.verify_user_password(user.password_hash, password):
                raise InvalidLoginCredentials

            payload = {"user_uuid": user.uuid}

            access_token = generate_access_token(payload)

        return access_token

    @build_response
    def logout(self, access_token: str) -> None:
        ACCESS_TOKEN_BLACKLIST.add(access_token)

    @staticmethod
    def verify_user_password(user_password_hash: "User.password_hash", password: str) -> bool:
        return check_password_hash(user_password_hash, password)
