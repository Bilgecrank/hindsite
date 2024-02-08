"""
Class definition for the user table
"""
import datetime

from typing import Optional
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship



class User(db.Model):
    """
    Defines the core user model to include basic user information.

    Attributes:
        id: **int** Primary key id for table, initialized automatically.
        first_name: **str** User's first name.
        last_name: **str** User's last name.
        display_name: **str** User's publicly identifiable name.
        email: **str** User's email address, used for login verification.
        last_login: **datetime** Datetime of the User's last login into the system.
        verified: **bool** Whether or not the user's email address has been verified.
    """
    __tablename__ = 'user'

    id: Mapped[intpk] = mapped_column(init=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    display_name: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    last_login: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now())
    verified: Mapped[bool] = mapped_column(default=False)
    password = relationship("Password", back_populates='password')

