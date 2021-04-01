from src.make_a_comment.domain.comment import Comment
from src.make_a_comment.domain.user import User


def test_user_persistence(session, user_data):

    user = User(**user_data)
    session.add(user)
    session.commit()

    queried_user = session.query(User).filter_by(uuid=user.uuid).first()

    assert queried_user == user

    session.delete(user)
    session.commit()


def test_comment_persistence(session, user_data):

    user = User(**user_data)
    session.add(user)
    session.commit()

    comment = Comment("test_comment_persistence")
    comment.user_uuid = user.uuid
    session.add(comment)
    session.commit()

    queried_comment = session.query(
        Comment).filter_by(uuid=comment.uuid).first()

    assert queried_comment == comment

    # session.delete(comment)
    session.delete(user)
    session.commit()


def test_user_can_make_a_comment_and__persistence(session, user_data):
    user = User(**user_data)
    comment = Comment("test_user_can_make_a_comment_and__persistence")
    user.make_a_comment(comment)
    session.add(user)
    session.commit()

    queried_user = session.query(User).filter_by(uuid=user.uuid).first()
    queried_comment = session.query(
        Comment).filter_by(uuid=comment.uuid).first()

    assert queried_comment == comment
    assert queried_user == user

    # session.delete(comment)
    session.delete(user)
    session.commit()
