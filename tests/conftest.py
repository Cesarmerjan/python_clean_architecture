import os
from datetime import datetime
import pytest


from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from src.make_a_comment.adapters.orm import start_mapper, metadata

from src.make_a_comment.domain.user import User

from src.make_a_comment.adapters.controllers.api import create_api


@pytest.fixture(scope="function")
def user_data():
    return {
        "name": "Test",
        "email": "test@gmail.com",
        "password": "easypass"
    }


@pytest.fixture(scope="function")
def user(user_data):
    return User(**user_data)


@pytest.fixture(scope="session")
def database_uri():
    return "sqlite:///db_test.sqlite"


@pytest.fixture(scope="session")
def engine(database_uri):
    return create_engine(database_uri)


@pytest.fixture(scope="session")
def connection(engine):
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="session")
def mapper(engine):
    start_mapper()
    metadata.create_all(engine)

    yield

    clear_mappers()
    metadata.drop_all(engine)


@pytest.fixture
def session(connection, mapper):

    # transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.rollback()
    session.close()
    # transaction.rollback()


@pytest.fixture
def session_factory(engine, mapper):
    yield sessionmaker(bind=engine,
                       autocommit=False,
                       autoflush=False)


@pytest.fixture
def api(connection, mapper):
    api = create_api('test')
    api_context = api.app_context()
    api_context.push()
    yield api
    api_context.pop()


@pytest.fixture
def api_client(api):
    api_client = api.test_client()
    api_client.testing = True
    yield api_client
