"""
Class definition for the user table
"""
import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from src.main import db, intpk


class User(db.Model):
    """
    Defines the core user model to include basic user information.
    """
    __tablename__ = 'user'

    id: Mapped[intpk] = mapped_column(init=False)
    "Primary key id for table."
    first_name: Mapped[str] = mapped_column(String(50))
    "User's first name."
    last_name: Mapped[str] = mapped_column(String(50))
    "User's last name."
    display_name: Mapped[str] = mapped_column(String(50))
    "User's publicly identifiable name."
    email: Mapped[str] = mapped_column(String(50), unique=True)
    "User's email address, used for login verification."
    last_login: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True))
    "Datetime the User's last login into the system."
    verified: Mapped[bool] = mapped_column(default=False)
    "Whether or not the user's email address has been verified."

