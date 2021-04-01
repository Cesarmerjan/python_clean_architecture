from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.serializer.comment import comment_serializer
from src.make_a_comment.domain.user import User
from src.make_a_comment.serializer.user import user_serializer


def test_comment_serializer_load():

    request = {"text": "test_comment_serializer"}

    parsed_request = comment_serializer.load(request)

    comment = Comment(**parsed_request)

    assert comment.text == parsed_request["text"]
    assert comment.uuid
    assert comment.datetime


def test_comment_serializer_dump():

    comment = Comment("test_comment_serializer_dump")

    response = comment_serializer.dump(comment)

    assert comment.text == response["text"]
    assert comment.uuid == response["uuid"]
    assert str(comment.datetime) == response["datetime"].replace("T", " ")


def test_comment_serializer_dump_many():

    comment1 = Comment("test_comment_serializer_dump_many")
    comment2 = Comment("test_comment_serializer_dump_many")

    response = comment_serializer.dump([comment1, comment2], many=True)

    assert len(response) == 2

    assert comment1.text == response[0]["text"]
    assert comment1.uuid == response[0]["uuid"]
    assert str(comment1.datetime) == response[0]["datetime"].replace("T", " ")

    assert comment2.text == response[1]["text"]
    assert comment2.uuid == response[1]["uuid"]
    assert str(comment2.datetime) == response[1]["datetime"].replace("T", " ")


def test_user_serializer_load():

    request = {"name": "test",
               "email": "test@email.com",
               "password": "easypass",
               }

    parsed_request = user_serializer.load(request)

    user = User(**parsed_request)

    assert user.uuid
    assert user.name == parsed_request["name"]
    assert user.email == parsed_request["email"]
    assert user.admin == False
    assert user.password_hash


def test_user_serializer_dump():

    user_data = {"name": "test",
                 "email": "test@email.com",
                 "password": "easypass",
                 }

    user = User(**user_data)

    response = user_serializer.dump(user)

    assert user.uuid
    assert user.name == response["name"]
    assert user.email == response["email"]
    assert user.admin == False
    assert user.password_hash


def test_user_serializer_dump_many():

    user_data = {"name": "test",
                 "email": "test@email.com",
                 "password": "easypass",
                 }

    user1 = User(**user_data)
    user2 = User(**user_data)

    response = user_serializer.dump([user1, user2], many=True)

    assert user1.uuid
    assert user1.name == response[0]["name"]
    assert user1.email == response[0]["email"]
    assert user1.admin == False
    assert user1.password_hash

    assert user2.uuid
    assert user2.name == response[1]["name"]
    assert user2.email == response[1]["email"]
    assert user2.admin == False
    assert user2.password_hash


def test_user_serializer_dump_with_comments():

    user_data = {"name": "test",
                 "email": "test@email.com",
                 "password": "easypass",
                 }

    user = User(**user_data)
    user.make_a_comment(Comment("test_user_serializer_dump_with_comments"))
    user.make_a_comment(Comment("test_user_serializer_dump_with_comments"))

    response = user_serializer.dump(user)

    assert user.uuid
    assert user.name == response["name"]
    assert user.email == response["email"]
    assert user.admin == False
    assert user.password_hash
    assert len(user.comments) == len(response["comments"])
