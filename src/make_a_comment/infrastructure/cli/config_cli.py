from src.config import (
    SECRET_KEY,
    PROD_DATABASE_URI,
    DEV_DATABASE_URI,
    TEST_DATABASE_URI
)


class Config:
    SECRET_KEY = SECRET_KEY

    PROGRAM_NAME = "make_a_comment"
    PROGRAM_USAGE = \
        """
.
---------------------------------------------------
Program name:

%(prog)s
---------------------------------------------------
Usage:

You can use this cli to interact with the
application's use cases
"""
    PROGRAM_DESCRIPTION = \
        """
---------------------------------------------------
Description:

CLI for an application made with
Clean Architecture and Python
---------------------------------------------------
"""


class Development(Config):
    DATABASE_URI = DEV_DATABASE_URI


class Test(Config):
    DATABASE_URI = TEST_DATABASE_URI


class Production(Config):
    DATABASE_URI = PROD_DATABASE_URI


CLI_CONFIG = {
    "development": Development,
    "test": Test,
    "production": Production,
    "default": Development
}
