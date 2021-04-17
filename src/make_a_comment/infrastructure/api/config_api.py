from src.config import (
    SECRET_KEY,
    PROD_DATABASE_URI,
    DEV_DATABASE_URI,
    TEST_DATABASE_URI
)


class Config:
    SECRET_KEY = SECRET_KEY
    PROPAGATE_EXCEPTIONS = True

    def init(self):
        pass


class Development(Config):
    ENV = "development"
    DEBUG = True
    DATABASE_URI = DEV_DATABASE_URI


class Test(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URI = TEST_DATABASE_URI


class Production(Config):
    ENV = "production"
    DEBUG = False
    DATABASE_URI = PROD_DATABASE_URI


API_CONFIG = {
    "development": Development,
    "test": Test,
    "production": Production,
    "default": Development
}
