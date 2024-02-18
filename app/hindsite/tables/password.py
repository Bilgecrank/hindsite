"""
Class definition for the password table
"""
import datetime

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.hindsite.extensions import db, intpk


class Password(db.Model):  # pylint: disable=too-few-public-methods
    """
    Defines the password table to include password hashes and last changed passwords.

    Attributes:
        id: **int** Primary key id for table, initialized automatically.
        user_id: **int** Foreign key for relative user to the password.
        password: **str* Password stored as a hash.
        last_updated: **datetime** The last time the entry was updated.
        user: **User** Reference to user table entry.
    """
    __tablename__ = 'password'

    id: Mapped[intpk] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    password: Mapped[str] = mapped_column(String(63))
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                 default=datetime.datetime.now(),
                                 server_default=text(
                                 'CURRENT_TIMESTAMP ON UPDATE '
                                 'CURRENT_TIMESTAMP'))
    user = relationship('User', back_populates='password')
