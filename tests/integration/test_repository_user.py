import pytest

from src.make_a_comment.domain.user import User
from src.make_a_comment.adapters.repository.user import UserRepository

from sqlalchemy.exc import IntegrityError, NoResultFound


def test_user_repository_add(session, user_data):

    user_repository = UserRepository(session)

    user = User(**user_data)
    user_repository.add(user)

    session.commit()

    with pytest.raises(IntegrityError):
        user_repository.add(User(**user_data))
        assert session.commit()
    session.rollback()

    queried_user = session.query(User).filter_by(uuid=user.uuid).first()

    assert queried_user == user

    session.delete(user)
    session.commit()


def test_user_repository_get_by(session, user_data):

    user_repository = UserRepository(session)

    user = User(**user_data)
    session.add(user)
    session.commit()

    queried_user = user_repository.get_by(uuid=user.uuid)

    assert queried_user == user

    with pytest.raises(NoResultFound):
        assert user_repository.get_by(uuid="wrong")
    session.rollback()

    session.delete(user)
    session.commit()


def test_user_repository_get_all(session, user_data):

    user_repository = UserRepository(session)

    user = User(**user_data)
    session.add(user)
    session.commit()

    queried_users = user_repository.get_all()

    assert type(queried_users) == list
    for user in queried_users:
        assert isinstance(user, User)

    session.delete(user)
    session.commit()


def test_user_repository_delete(session, user_data):

    user_repository = UserRepository(session)

    user = User(**user_data)
    session.add(user)
    session.commit()

    user_repository.delete(user)
    session.commit()

    queried_user = session.query(User).filter_by(uuid=user.uuid).first()

    assert queried_user == None


def test_user_repository_update(session, user_data):

    user_repository = UserRepository(session)

    user = User(**user_data)
    session.add(user)
    session.commit()

    queried_user = session.query(User).filter_by(uuid=user.uuid).first()

    updated_user = user_repository.update(
        queried_user, **{"name": "New Name"})
    session.add(updated_user)
    session.commit()

    assert updated_user.name == "New Name"
    assert updated_user == user

    session.delete(user)
    session.commit()
