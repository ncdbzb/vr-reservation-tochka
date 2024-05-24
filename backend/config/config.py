from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

CORS_ORIGINS = os.environ.get("CORS_ORIGINS")

if CORS_ORIGINS:
    CORS_ORIGINS = eval(CORS_ORIGINS)
else:
    print('CORS_ORIGINS not set in environment')