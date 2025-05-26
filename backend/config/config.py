from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SERVER_DOMAIN = os.environ.get("SERVER_DOMAIN")

SECRET_JWT = os.environ.get("SECRET_JWT")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
COOKIE_LIFETIME = int(os.environ.get("COOKIE_LIFETIME"))
JWT_TOKEN_LIFETIME = int(os.environ.get("JWT_TOKEN_LIFETIME"))

REDIS_URL = os.environ.get("REDIS_URL")

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
