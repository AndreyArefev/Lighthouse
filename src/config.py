from dotenv import load_dotenv
from datetime import timedelta

import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_URL = os.environ.get("DB_URL")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
AUTHJWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
AUTHJWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
SECRET_KEY='secret'
ALGORITHM='HS256'






