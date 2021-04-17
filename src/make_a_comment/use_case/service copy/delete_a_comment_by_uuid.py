from copy import deepcopy
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface


def delete_a_comment_by_uuid(comment_uuid: "Comment.uuid", comment_uow: UoWInterface) -> None:
    with comment_uow:
        comment = comment_uow.repository.get_by(uuid=comment_uuid)
        comment_uow.repository.delete(comment)
        comment_uow.commit()
