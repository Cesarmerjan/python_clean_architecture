from copy import deepcopy
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface


def update_a_comment(comment_uuid: "Comment.uuid", new_text: str, comment_uow: UoWInterface) -> Comment:
    with comment_uow:
        comment = comment_uow.repository.get_by(uuid=comment_uuid)
        comment.text = new_text
        response = deepcopy(comment)
        comment_uow.repository.add(comment)
        comment_uow.commit()
        return response
