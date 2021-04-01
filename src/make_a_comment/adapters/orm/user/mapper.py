from sqlalchemy.orm import mapper, relationship
from .table import users_table
from src.make_a_comment.domain.user import User
from src.make_a_comment.domain.comment import Comment


mapper(User, users_table,
       properties={
           "comments": relationship(Comment, cascade="all,delete",
                                    backref="users", collection_class=set)
       })
