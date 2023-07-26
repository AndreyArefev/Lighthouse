from datetime import timedelta
from os import environ as env

from dotenv import load_dotenv

load_dotenv()

MODE = env.get("MODE") #DEV
LOG_LEVEL = env.get("LOG_LEVEL")

DB_HOST = env.get("DB_HOST")
DB_PORT = env.get("DB_PORT")
DB_USER = env.get("DB_USER")
DB_PASS = env.get("DB_PASS")
DB_NAME = env.get("DB_NAME")
SQLITE_DB_URL = env.get("SQLITE_DB_URL")

TEST_DB_HOST = env.get("TEST_DB_HOST")
TEST_DB_PORT = env.get("TEST_DB_PORT")
TEST_DB_USER = env.get("TEST_DB_USER")
TEST_DB_PASS = env.get("TEST_DB_PASS")
TEST_DB_NAME = env.get("TEST_DB_NAME")
TEST_SQLITE_DB_URL = env.get("TEST_SQLITE_DB_URL")

REDIS_HOST = env.get("REDIS_HOST")
REDIS_PORT = env.get("REDIS_PORT")

SMTP_HOST = env.get("SMTP_HOST")
SMTP_PORT = env.get("SMTP_PORT")
SMTP_USER = env.get("SMTP_USER")
SMTP_PASS = env.get("SMTP_PASS")

SECRET_KEY_CONFIRM_TOKEN = env.get("SECRET_KEY_CONFIRM_TOKEN")
AUTHJWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
AUTHJWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
SECRET_KEY='secret'
ALGORITHM='HS256'
