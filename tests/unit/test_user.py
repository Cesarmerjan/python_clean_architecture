import pytest
from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment
from werkzeug.security import check_password_hash


def test_create_a_user(user_data, user):
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]


def test_user_password_hash(user_data, user):
    assert check_password_hash(user.password_hash, user_data["password"])


def test_user_can_make_a_comment(user):
    comment = Comment("First Comment")
    user.make_a_comment(comment)
    assert comment in user.comments


def test_user_cannot_read_the_password(user):
    with pytest.raises(AttributeError):
        assert user.password


def test_user_can_change_password(user_data):
    user = User(**user_data)
    new_password = "new password"
    user.password = new_password
    assert check_password_hash(user.password_hash, new_password)
