import pytest
import jwt
from src.make_a_comment.use_case import interactor
from src.make_a_comment.utils.jwt_handler import validate_access_token


def test_system():
    system = interactor.start_system()
    user = interactor.create_a_user(name="guest", email="guest@gmail.com",
                                    password="hard to guess")

    interactor.register_a_user(system, user)

    access_token = interactor.user_login(user, "hard to guess")
    assert interactor.verify_access_token(access_token)

    user_uuid = interactor.get_user_uuid_from_jwt(access_token)

    assert user_uuid == user.uuid

    comment = interactor.make_a_user_comment(
        user, "First Comment", access_token)

    assert comment in interactor.view_comments_on_system(system)

    queried_comment = interactor.get_a_user_comment_by_uuid(user, comment.uuid)

    assert queried_comment == comment

    user2 = interactor.create_a_user(name="guest2", email="guest2@gmail.com",
                                     password="hard to guess")

    interactor.register_a_user(system, user2)

    with pytest.raises(ValueError):
        assert interactor.make_a_user_comment(user, "First Comment")

    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        assert interactor.make_a_user_comment(user,
                                              "First Comment", access_token + "invalid")
