from types import GeneratorType
from . import service
from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.domain.system import System
from src.make_a_comment.utils.jwt_handler import login_required


def create_a_user(name: str, email: str, password: str) -> User:
    user = service.create_a_user(name, email, password)
    return user


@login_required
def make_a_user_comment(user: User, text: str, access_token: str) -> Comment:
    comment = service.make_a_user_comment(user, text)
    return comment


@login_required
def delete_a_user_comment_by_uuid(user: User, uuid: "Comment.uuid", access_token: str) -> None:
    comment = service.delete_a_user_comment_by_uuid(user, uuid)
    user.comments.remove(comment)


@login_required
def update_a_comment(comment: Comment, new_text: str, access_token: str) -> Comment:
    comment = service.update_a_comment(comment, new_text)
    return comment


def get_a_user_comment_by_uuid(user: User, uuid: "Comment.uuid") -> Comment:
    comment = service.get_a_user_comment_by_uuid(user, uuid)
    return comment


def get_a_user_by_uuid(system: System, uuid: "User.uuid"):
    user = service.get_a_user_by_uuid(system, uuid)
    return user


def start_system():
    return service.start_system()


def register_a_user(system: System, user: User) -> None:
    service.register_a_user(system, user)


def view_comments_on_system(system) -> GeneratorType:
    return service.view_comments_on_system(system)


def user_login(user: User, password: str) -> str:
    return service.user_login(user, password)


def user_logout():
    return service.user_logout()


def verify_user_password(user: User, password: str) -> bool:
    return service.verify_user_password(user, password)


def get_user_uuid_from_jwt(access_token):
    return service.get_user_uuid_from_jwt(access_token)


def verify_access_token(access_token):
    return service.validate_access_token(access_token)
