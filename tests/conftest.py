import pytest

from src.make_a_comment.domain.system import System
from src.make_a_comment.domain.user import User


@pytest.fixture(scope="session")
def user_data():
    return {
        "name": "Cesar",
        "email": "cesarmerjan@gmail.com",
        "password": "easypass"
    }


@pytest.fixture(scope="session")
def user(user_data):
    return User(**user_data)


@pytest.fixture(scope="session")
def system(user):
    system = System()
    system.register_a_user(user)
    return system
