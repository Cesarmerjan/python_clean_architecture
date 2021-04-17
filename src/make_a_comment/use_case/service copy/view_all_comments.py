from typing import List
from copy import deepcopy
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface


def view_all_comments(comment_uow: UoWInterface) -> List[Comment]:
    with comment_uow:
        comments = comment_uow.repository.get_all()
        response = deepcopy(comments)
    return response
