import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DB_USER_TEST = os.environ.get("DB_TEST_USER")
DB_PASS_TEST = os.environ.get("DB_TEST_PASS")
DB_HOST_TEST = os.environ.get("DB_TEST_HOST")
DB_PORT_TEST = os.environ.get("DB_TEST_PORT")
DB_NAME_TEST = os.environ.get("DB_TEST_NAME")

JWT_SECRET = os.environ.get("JWT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_TOKEN_ALGORITHM = "HS256"
VERSION_PREFIX = "/v1"
