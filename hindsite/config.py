"""
Sets up Flask config variables to run the web application.
"""

import os
from dotenv import load_dotenv


class Config:  # pylint: disable=too-few-public-methods
    """
    Base configuration class. Contains default config settings
    """
    load_dotenv()
    database_uri = ("mysql+pymysql://"
                    + os.environ['MYSQLUSER'] + ":"
                    + os.environ['MYSQL_ROOT_PASSWORD'] + "@"
                    + os.environ['MYSQLHOST'] + ":"
                    + os.environ['MYSQLPORT'] + "/"
                    + os.environ['MYSQL_DATABASE'])
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = database_uri
