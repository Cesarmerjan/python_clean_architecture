from .sqlalchemy import SqlAlchemyUoW
from src.make_a_comment.adapters.repository.comment import CommentRepository


class CommentUoW(SqlAlchemyUoW):
    def __enter__(self):
        return super().__enter__(CommentRepository)
