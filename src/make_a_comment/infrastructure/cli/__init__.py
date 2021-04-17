import argparse

from src.make_a_comment.adapters.orm import start_mapper, metadata
from src.make_a_comment.infrastructure.drivers.sqlalchemy import make_engine, make_session_factory

from .parsers import register_parsers

from .config_cli import CLI_CONFIG


def init_cli(config_name="default"):
    config_obj = CLI_CONFIG[config_name]
    start_mapper()
    engine = make_engine(config_obj.DATABASE_URI)
    metadata.create_all(engine)

    parser = argparse.ArgumentParser(
        prog=config_obj.PROGRAM_NAME,
        usage=config_obj.PROGRAM_USAGE,
        description=config_obj.PROGRAM_DESCRIPTION,
        epilog="Copyrights @CesarMerjan",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
        allow_abbrev=False)

    subparsers = parser.add_subparsers()

    register_parsers(subparsers)

    options = parser.parse_args()

    options.session_factory = make_session_factory(engine)

    options.func(options)
