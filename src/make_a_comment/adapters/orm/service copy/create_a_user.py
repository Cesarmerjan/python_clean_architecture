from copy import deepcopy
from src.make_a_comment.domain.user import User
from src.make_a_comment.adapters.unit_of_work.interface import UoWInterface


def create_a_user(name: str, email: str, password: str, user_uow: UoWInterface, admin: bool = None) -> User:
    with user_uow:
        user = user_uow.repository.add(
            User(name, email, password, admin)
        )
        response = deepcopy(user)
        user_uow.commit()
    return response
