from typing import Set
import uuid
from werkzeug.security import generate_password_hash
from .comment import Comment


class User:

    def __init__(self, name: str, email: str, password: str, admin: bool = False):
        self.uuid = str(uuid.uuid4())  # 36 char
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)  # 128 char
        self.comments = set()  # type: Set[Comment]
        self.admin = admin

    def __repr__(self):
        return f"<User {self.uuid}>"

    def __str__(self):
        return f"user name: {self.name}\nuser email: {self.email}"

    def __eq__(self, other: "User") -> bool:
        if not isinstance(other, User):
            return False
        return other.uuid == self.uuid

    def __hash__(self):
        return hash(self.uuid)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def make_a_comment(self, comment: Comment) -> None:
        if not comment in self.comments:
            self.comments.add(comment)
