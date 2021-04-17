import abc
from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment

from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface


class UserServiceInterface(metaclass=abc.ABCMeta):

    user_uow: UoWInterface

    @abc.abstractmethod
    def register_user(self, name: str, email: str, password: str, admin: bool = None) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_uuid(self, user_uuid: "User.uuid") -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def make_a_comment(self, user_uuid: "User.uuid", text: str) -> Comment:
        raise NotImplementedError

    @abc.abstractmethod
    def login(self, email: "User.email", password: str) -> "access_token":
        raise NotImplementedError

    @abc.abstractmethod
    def logout(self, access_token: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def verify_user_password(self, user_password_hash: "User.password_hash", password: str) -> bool:
        raise NotImplementedError
