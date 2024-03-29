"""
    Helper module for imports.
"""
import flask_login
from flask_bootstrap import Bootstrap5
from typing_extensions import Annotated
import sqlalchemy.orm
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from flask_sqlalchemy import SQLAlchemy

# BOOTSTRAP INSTANTIATION

bootstrap = Bootstrap5()

# FLASK_LOGIN LOGIN MANAGER INSTANTIATION.

login_manager = flask_login.LoginManager()

# SQLALCHEMY EXTENSION SET-UP.


class Base(DeclarativeBase, MappedAsDataclass):  # pylint: disable=too-few-public-methods
    """
    The base model for the classes to be declared.
    """

# pylint: disable=invalid-name
intpk = Annotated[int, sqlalchemy.orm.mapped_column(primary_key=True,
                                                    autoincrement=True)]
# pylint: enable=invalid-name

db = SQLAlchemy(model_class=Base)
