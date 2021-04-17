from flask import Flask

from .config_api import API_CONFIG
from .resources import register_resources

from src.make_a_comment.infrastructure.drivers.sqlalchemy import make_engine, make_session_factory
from src.make_a_comment.adapters.orm import start_mapper, metadata


def create_api(config_name="default"):
    start_mapper()

    api = Flask(__name__)
    api.config.from_object(API_CONFIG[config_name])

    engine = make_engine(api.config.get("DATABASE_URI"))
    metadata.create_all(engine)

    api.session_factory = make_session_factory(engine)

    register_resources(api)

    return api
