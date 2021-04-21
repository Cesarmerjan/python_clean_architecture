from werkzeug.security import check_password_hash
from src.make_a_comment.domain.user import User


def verify_user_password(user_password_hash: "User.password_hash", password: str) -> bool:
    return check_password_hash(user_password_hash, password)
