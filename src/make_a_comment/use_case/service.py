from types import GeneratorType
from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.domain.system import System
from werkzeug.security import check_password_hash
from src.make_a_comment.utils.jwt_handler import generate_access_token, get_jwt_pay_load, validate_access_token


def create_a_user(name: str, email: str, password: str) -> User:
    user = User(name, email, password)
    return user


def make_a_user_comment(user: User, text: str) -> Comment:
    comment = Comment(text)
    user.make_a_comment(comment)
    return comment


def delete_a_user_comment_by_uuid(user: User, uuid: "Comment.uuid") -> None:
    comment = get_a_user_comment_by_uuid(user, uuid)
    user.comments.remove(comment)


def update_a_comment(comment: Comment, new_text: str) -> Comment:
    comment.text = new_text
    return comment


def get_a_user_comment_by_uuid(user: User, uuid: "Comment.uuid") -> Comment:
    comment = next(
        (comment
         for comment in user.comments
         if comment.uuid == uuid),
        None)
    return comment


def get_a_user_by_uuid(system: System, uuid: "User.uuid"):
    user = next(
        (user
         for user in system.users
         if user.uuid == uuid),
        None)
    return user


def start_system():
    return System()


def register_a_user(system: System, user: User) -> None:
    system.register_a_user(user)


def view_comments_on_system(system) -> GeneratorType:
    for user in system.users:
        for comment in user.comments:
            yield comment


def user_login(user: User, password: str) -> str:
    if not verify_user_password(user, password):
        raise ValueError("Bad Authentication")
    return generate_access_token({"user_uuid": user.uuid})


def verify_access_token(access_token):
    return validate_access_token(access_token)


def user_logout():
    "revoke token"


def verify_user_password(user: User, password: str) -> bool:
    return check_password_hash(user.password_hash, password)


def get_user_uuid_from_jwt(access_token):
    pay_load = get_jwt_pay_load(access_token)
    return pay_load["user_uuid"]
