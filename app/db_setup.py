import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing_extensions import Annotated
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, mapped_column
from dotenv import load_dotenv

# Included to load .env environment variables for local dev
load_dotenv()

# Location agnostic URI that loads either the .env file, or if
# it's not included loads the variables set by the OS. In the
# case of Railway.app, the variables set by the database and
# linked to the app.
database_uri = ("mysql+pymysql://"
                + os.environ['MYSQLUSER'] + ":"
                + os.environ['MYSQL_ROOT_PASSWORD'] + "@"
                + os.environ['MYSQLHOST'] + ":"
                + os.environ['MYSQLPORT'] + "/"
                + os.environ['MYSQL_DATABASE'])

# Needed to redirect default paths to maintain the proposed folder structure
# since Flask looks for static and templates in the root folder of the app
template_dir = os.path.abspath('app/templates')
static_dir = os.path.abspath('app/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Sets the database URI to match whatever environment it's in
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False


class Base(DeclarativeBase, MappedAsDataclass):
    """
    The base model for the classes to be declared.
    """
    pass


intpk = Annotated[int, mapped_column(primary_key=True,
                                     autoincrement=True)]
db = SQLAlchemy(app, model_class=Base)
