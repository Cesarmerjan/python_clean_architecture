from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def make_engine(database_uri: str):
    engine = create_engine(database_uri)
    return engine


def make_session_factory(engine, autocommit: bool = False, autoflush: bool = False):
    session_factory = sessionmaker(
        bind=engine, autocommit=autocommit, autoflush=autoflush)
    return session_factory
