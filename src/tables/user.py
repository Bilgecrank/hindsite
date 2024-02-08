"""
Class definition for the users class
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
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    display_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    last_login: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True))
    verified: Mapped[bool] = mapped_column(default=False)

