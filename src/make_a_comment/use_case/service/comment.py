from typing import List
from copy import deepcopy
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface

from .comment_interface import CommentServiceInterface


class CommentService(CommentServiceInterface):

    def __init__(self, comment_uow: UoWInterface):
        self.uow = comment_uow

    # delete_a_comment_by_uuid
    def delete_comment_by_uuid(self, comment_uuid: "Comment.uuid") -> None:
        with self.uow:
            comment = self.uow.repository.get_by(uuid=comment_uuid)
            self.uow.repository.delete(comment)
            self.uow.commit()

    # get_a_comment_by_uuid
    def get_comment_by_uuid(self, comment_uuid: "Comment.uuid") -> Comment:
        with self.uow:
            comment = self.uow.repository.get_by(uuid=comment_uuid)
            comment_copy = deepcopy(comment)
        return comment_copy

    # update_a_comment
    def update_comment_by_uuid(self, comment_uuid: "Comment.uuid", new_text: str) -> Comment:
        with self.uow:
            comment = self.uow.repository.get_by(uuid=comment_uuid)
            comment.text = new_text
            comment_copy = deepcopy(comment)
            self.uow.repository.add(comment)
            self.uow.commit()
            return comment_copy

    # view_all_comments
    def get_all_comments(self) -> List[Comment]:
        with self.uow:
            comments = self.uow.repository.get_all()
            comment_copy = deepcopy(comments)
        return comment_copy
