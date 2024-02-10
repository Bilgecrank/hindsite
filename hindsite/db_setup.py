"""
Back-end variables to set up database interactions.
"""

import os
from flask import Flask
from sqlalchemy import Table, Column, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from typing_extensions import Annotated
import sqlalchemy.orm
from dotenv import load_dotenv

# Included to load .env environment variables for local dev
load_dotenv()

# Location agnostic URI that loads either the .env file, or if
# it's not included loads the variables set by the OS. In the
# case of Railway.hindsite, the variables set by the database and
# linked to the hindsite.
database_uri = ("mysql+pymysql://"
                + os.environ['MYSQLUSER'] + ":"
                + os.environ['MYSQL_ROOT_PASSWORD'] + "@"
                + os.environ['MYSQLHOST'] + ":"
                + os.environ['MYSQLPORT'] + "/"
                + os.environ['MYSQL_DATABASE'])

# Needed to redirect default paths to maintain the proposed folder structure
# since Flask looks for static and templates in the root folder of the hindsite
template_dir = os.path.abspath('db_test_templates')
static_dir = os.path.abspath('static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Sets the database URI to match whatever environment it's in
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False


class Base(sqlalchemy.orm.DeclarativeBase, sqlalchemy.orm.MappedAsDataclass):  # pylint: disable=too-few-public-methods
    """
    The base model for the classes to be declared.
    """


# Defines association table for the User/Group relationship
user_membership = Table(
    'user_membership',
    Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('group_id', ForeignKey('group.id'), primary_key=True)
)

# pylint: disable=invalid-name
intpk = Annotated[int, sqlalchemy.orm.mapped_column(primary_key=True,
                                                    autoincrement=True)]
db = SQLAlchemy(app, model_class=Base)
