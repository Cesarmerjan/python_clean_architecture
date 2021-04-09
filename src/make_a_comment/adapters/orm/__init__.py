"""Responsible for mapping objects with database tables"""
from sqlalchemy import MetaData


metadata = MetaData()


def start_mapper():
    from .user import mapper
    from .comment import mapper
