from copy import deepcopy
from src.make_a_comment.domain.user import User
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface


def get_a_user_by_uuid(user_uuid: "User.uuid", user_uow: UoWInterface):
    with user_uow:
        user = user_uow.repository.get_by(uuid=user_uuid)
        # This (user.comments) needs to be here because of the relationship
        # This query all comments of the user before creating the deepcopy
        # If this is not here you will get the following error:
        # sqlalchemy.orm.exc.DetachedInstanceError
        user.comments
        response = deepcopy(user)
    return response
