from sqlalchemy.orm import mapper
from .table import comments_table
from src.make_a_comment.domain.comment import Comment

mapper(Comment, comments_table)
