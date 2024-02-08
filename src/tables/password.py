"""
Class definition for the password table
"""
import datetime

from sqlalchemy import DateTime, ForeignKey, String, text, relationship
from sqlalchemy.orm import Mapped, mapped_column

from src.main import db, intpk


class Password(db.Model):
    """
    Defines the password table to include password hashes and last changed passwords.
    """
    __tablename__ = 'password'

    id: Mapped[intpk] = mapped_column(int=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    password: Mapped[str] = mapped_column(String(63))
    last_updated: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                            server_default=text('CURRENT_TIMESTAMP ON UPDATE '
                                                                           'CURRENT_TIMESTAMP'))
    user = relationship('User', back_populates='user')
