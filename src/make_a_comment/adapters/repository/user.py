from typing import List

from src.make_a_comment.domain.user import User
from .interface import RepositoryInterface


class UserRepository(RepositoryInterface):
    def __init__(self, session):
        self.session = session

    def add(self, user: User) -> User:
        self.session.add(user)
        return user

    def get_by(self, **kwargs) -> User:
        return self.session.query(User).filter_by(**kwargs).one()

    def get_all(self) -> List[User]:
        return self.session.query(User).all()

    def delete(self, user: User) -> None:
        self.session.delete(user)

    def update(self, user: User, **kwargs) -> User:
        for attr, value in kwargs.items():
            setattr(user, attr, value)
        self.session.add(user)
        return user
