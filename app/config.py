"""
    Base configuration class. Contains default config settings
"""

import os
import secrets
from dotenv import load_dotenv

load_dotenv()
database_uri = ("mysql+pymysql://"
                + os.environ['MYSQLUSER'] + ":"
                + os.environ['MYSQL_ROOT_PASSWORD'] + "@"
                + os.environ['MYSQLHOST'] + ":"
                + os.environ['MYSQLPORT'] + "/"
                + os.environ['MYSQL_DATABASE'])


class Config:  # pylint: disable=too-few-public-methods
    """
        Base configuration class. Contains default config settings. Use
        os.getenv to have persistent sessions between restarts. Use 
        secrets.token_hex(32) if you want to reset the session every time.
    """
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    # SECRET_KEY = os.getenv('SECRET_KEY')
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = database_uri
