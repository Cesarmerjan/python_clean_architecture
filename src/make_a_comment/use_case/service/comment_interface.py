import abc
from typing import List
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface


class CommentServiceInterface(metaclass=abc.ABCMeta):

    comment_uow: UoWInterface

    @abc.abstractmethod
    def delete_comment_by_uuid(self, comment_uuid: "Comment.uuid") -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_comment_by_uuid(self, comment_uuid: "Comment.uuid") -> Comment:
        raise NotImplementedError

    @abc.abstractmethod
    def update_comment_by_uuid(self, comment_uuid: "Comment.uuid", new_text: str) -> Comment:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_comments(self) -> List[Comment]:
        raise NotImplementedError
