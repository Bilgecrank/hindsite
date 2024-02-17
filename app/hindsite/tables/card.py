"""
Defines the model for the cards and their relationships to others tables in the database.
"""

from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.hindsite.tables.base import db, intpk


class Card(db.Model):  # pylint: disable=too-few-public-methods
    """
    The Card holds comments and reactions from other users in the application.
    """
    __tablename__ = 'card'

    id: Mapped[intpk] = mapped_column(init=False)
    field_id: Mapped[int] = mapped_column(ForeignKey('field.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user.id'))
    message_body: Mapped[str] = mapped_column(String(6000))
    card_status: Mapped[str] = mapped_column(String(50))
    archived: Mapped[bool] = mapped_column(default=False)
    field = relationship('Field', back_populates='cards')
    author = relationship('User', foreign_keys=[author_id])
    owner = relationship('User', foreign_keys=[owner_id])
