from types import GeneratorType
from src.make_a_comment.use_case import service
from src.make_a_comment.utils.jwt_handler import validate_access_token


def test_can_service_create_a_user(user_data):
    user = service.create_a_user(**user_data)
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]


def test_can_service_make_a_user_comment(user):
    text = "test_can_service_make_an_user_comment"
    comment = service.make_a_user_comment(user, text)
    assert comment in user.comments


def test_can_service_delete_a_user_comment(user):
    initial_numer_of_comments = len(user.comments)
    text = "test_can_service_delete_a_user_comment"
    comment = service.make_a_user_comment(user, text)

    service.delete_a_user_comment_by_uuid(user, comment.uuid)

    assert len(user.comments) == initial_numer_of_comments


def test_can_service_update_a_comment(user):
    text = "test_can_service_update_a_comment"
    comment = service.make_a_user_comment(user, text)

    new_comment = service.update_a_comment(
        comment, text + "updated")

    queried_comment = service.get_a_user_comment_by_uuid(
        user, new_comment.uuid)

    assert queried_comment.text == comment.text


def test_can_service_get_a_user_comment_by_uuid(user):
    text = "test_can_service_get_a_user_comment_by_uuid"
    comment = service.make_a_user_comment(user, text)

    queried_comment = service.get_a_user_comment_by_uuid(user, comment.uuid)

    assert queried_comment == comment


def test_can_service_get_a_user_by_uuid(system, user):
    queried_user = service.get_a_user_by_uuid(system, user.uuid)
    assert queried_user == user


def test_can_service_register_a_user(system, user):
    service.register_a_user(system, user)
    assert user in system.users


def test_can_service_view_comments_on_system(system):
    assert isinstance(
        service.view_comments_on_system(system),
        GeneratorType)


def test_can_service_make_a_user_login(user, user_data):
    access_token = service.user_login(user, user_data["password"])
    assert validate_access_token(access_token)


def can_service_get_user_uuid_from_jwt(user, user_data):
    access_token = service.user_login(user, user_data["password"])
    user_uuid = service.get_user_uuid_from_jwt(access_token)
    assert user_uuid == user.uuid
