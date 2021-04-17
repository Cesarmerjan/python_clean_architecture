from copy import deepcopy

from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment

from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface
from .user_interface import UserServiceInterface

from werkzeug.security import check_password_hash
from src.make_a_comment.utils.jwt_handler import generate_access_token
from src.make_a_comment.utils.jwt_handler import ACCESS_TOKEN_BLACKLIST

from src.make_a_comment.exceptions.invalid_login_credentials import InvalidLoginCredentials


class UserService(UserServiceInterface):

    def __init__(self, user_uow: UoWInterface):
        self.uow = user_uow

    # create_a_user
    def register_user(self, name: str, email: str, password: str, admin: bool = None) -> User:
        with self.uow:
            user = self.uow.repository.add(
                User(name, email, password, admin)
            )
            user_copy = deepcopy(user)
            self.uow.commit()
        return user_copy

    # get_a_user_by_uuid
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

    # make_a_user_comment
    def make_a_comment(self, user_uuid: "User.uuid", text: str) -> Comment:
        with self.uow:
            user = self.uow.repository.get_by(uuid=user_uuid)
            comment = Comment(text)
            comment_copy = deepcopy(comment)
            user.make_a_comment(comment)
            self.uow.repository.add(user)
            self.uow.commit()
        return comment_copy

    # user_login
    def login(self, email: "User.email", password: str) -> "access_token":
        with self.uow:
            user = self.uow.repository.get_by(email=email)

            if not verify_user_password(user.password_hash, password):
                raise InvalidLoginCredentials

            payload = {"user_uuid": user.uuid}

            access_token = generate_access_token(payload)

        return access_token

    # user_logout
    def logout(self, access_token: str) -> None:
        ACCESS_TOKEN_BLACKLIST.add(access_token)

    # verify_user_password
    def verify_user_password(self, user_password_hash: "User.password_hash", password: str) -> bool:
        return check_password_hash(user_password_hash, password)
