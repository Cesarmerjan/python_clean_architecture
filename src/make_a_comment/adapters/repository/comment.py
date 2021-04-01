from typing import List

from src.make_a_comment.domain.comment import Comment
from .interface import RepositoryInterface


class CommentRepository(RepositoryInterface):
    def __init__(self, session):
        self.session = session

    def add(self, comment: Comment) -> Comment:
        self.session.add(comment)
        return comment

    def get_by(self, **kwargs) -> Comment:
        return self.session.query(Comment).filter_by(**kwargs).one()

    def get_all(self) -> List[Comment]:
        return self.session.query(Comment).all()

    def delete(self, comment: Comment) -> None:
        self.session.delete(comment)

    def update(self, comment: Comment, **kwargs) -> Comment:
        for attr, value in kwargs.items():
            setattr(comment, attr, value)
        self.session.add(comment)
        return comment
