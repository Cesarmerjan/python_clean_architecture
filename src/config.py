import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")

PROD_DATABASE_URI = os.environ.get("PROD_DATABASE_URI")
DEV_DATABASE_URI = os.environ.get("DEV_DATABASE_URI")
TEST_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")
