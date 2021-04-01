import pytest

from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.adapters.repository.comment import CommentRepository

from sqlalchemy.exc import IntegrityError, NoResultFound


def test_comment_repository_add(session, user_data):

    comment_repository = CommentRepository(session)

    user = User(**user_data)
    comment = Comment("test_comment_repository_add")
    comment.user_uuid = user.uuid
    comment_repository.add(comment)

    session.commit()

    queried_comment = session.query(
        Comment).filter_by(uuid=comment.uuid).first()

    assert queried_comment == comment

    session.delete(comment)
    session.commit()


def test_comment_repository_get_by(session, user_data):

    comment_repository = CommentRepository(session)

    user = User(**user_data)
    comment = Comment("test_comment_repository_get_by")
    comment.user_uuid = user.uuid
    session.add(comment)

    session.commit()

    queried_comment = comment_repository.get_by(uuid=comment.uuid)

    assert queried_comment == comment

    with pytest.raises(NoResultFound):
        assert comment_repository.get_by(uuid="wrong")
    session.rollback()

    session.delete(comment)
    session.commit()


def test_comment_repository_get_all(session, user_data):

    comment_repository = CommentRepository(session)

    user = User(**user_data)
    comment = Comment("test_comment_repository_get_all")
    comment.user_uuid = user.uuid
    session.add(comment)

    session.commit()

    queried_comments = comment_repository.get_all()

    assert type(queried_comments) == list
    for comment in queried_comments:
        assert isinstance(comment, Comment)

    session.delete(comment)
    session.commit()


def test_comment_repository_delete(session, user_data):

    comment_repository = CommentRepository(session)

    user = User(**user_data)
    comment = Comment("test_comment_repository_delete")
    comment.user_uuid = user.uuid
    session.add(comment)

    session.commit()

    comment_repository.delete(comment)
    session.commit()

    queried_comment = session.query(
        Comment).filter_by(uuid=comment.uuid).first()

    assert queried_comment == None


def test_comment_repository_update(session, user_data):

    comment_repository = CommentRepository(session)

    user = User(**user_data)
    comment = Comment("test_comment_repository_update")
    comment.user_uuid = user.uuid
    session.add(comment)

    session.commit()

    queried_comment = session.query(
        Comment).filter_by(uuid=comment.uuid).first()

    updated_comment = comment_repository.update(
        queried_comment, **{"text": "updated"})
    session.add(updated_comment)
    session.commit()

    assert updated_comment.text == "updated"
    assert updated_comment == comment

    session.delete(comment)
    session.commit()
