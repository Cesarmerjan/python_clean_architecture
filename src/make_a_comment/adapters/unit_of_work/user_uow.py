from .sqlalchemy import SqlAlchemyUoW
from src.make_a_comment.adapters.repository.user import UserRepository


class UserUoW(SqlAlchemyUoW):
    def __enter__(self):
        return super().__enter__(UserRepository)
