from copy import deepcopy
from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface


def make_a_user_comment(user_uuid: "User.uuid", text: str, user_uow: UoWInterface) -> Comment:
    with user_uow:
        user = user_uow.repository.get_by(uuid=user_uuid)
        comment = Comment(text)
        response = deepcopy(comment)
        user.make_a_comment(comment)
        user_uow.repository.add(user)
        user_uow.commit()
    return response
