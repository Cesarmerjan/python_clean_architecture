from datetime import datetime
from src.make_a_comment.domain.comment import Comment


def test_create_a_comment():
    text = "Primeiro comentário"
    comment = Comment(text)
    assert comment.text == text
    assert comment.datetime < datetime.now()
