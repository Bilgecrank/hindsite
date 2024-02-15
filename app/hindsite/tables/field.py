"""
Defines the model for the Field Table
"""
from sqlalchemy import ForeignKey, String

from app.hindsite import db
from app.hindsite.extensions import intpk
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Field(db.Model):
    """
    The field table is an archivable reference between boards and cards.
    """
    __tablename__ = 'field'

    id: Mapped[intpk] = mapped_column(init=False)
    board_id: Mapped[int] = mapped_column(ForeignKey('board.id'))
    name: Mapped[str] = mapped_column(String(50))
    archived: Mapped[bool] = mapped_column(default=False)
    board = relationship('Board', back_populates='fields')
    cards = relationship('Card', back_populates='field')
