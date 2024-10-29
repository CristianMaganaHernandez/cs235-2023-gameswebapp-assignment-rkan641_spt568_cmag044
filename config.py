from os import environ
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# Set env variables
class Config:
    FLASK_APP = environ.get("FLASK_APP"),
    FLASK_ENV = environ.get("FLASK_ENV"),
    SECRET_KEY = environ.get("SECRET_KEY"),
    TESTING = environ.get("TESTING"),
    WTF_CSRF_SECRET_KEY = environ.get("WTF_CSRF_SECRET_KEY")

    REPOSITORY = environ.get('REPOSITORY')
    # Database configuration
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    echo_string = environ.get('SQLALCHEMY_ECHO')
    SQLALCHEMY_ECHO = False
    if echo_string.lower().strip() == "true":
        SQLALCHEMY_ECHO = True