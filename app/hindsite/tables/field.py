"""
Defines the model for the Field Table
"""
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.hindsite.extensions import db, intpk


class Field(db.Model):  # pylint: disable=too-few-public-methods
    """
    The field table is an archivable reference between boards and cards.
    Attributes:
        id: **int** Primary Key of the field.
        board_id: **int** Foreign Key referencing the board this field belongs to.
        name: **str** Name of the field.
        archived: **bool** Whether the field has been 'deleted'.
        board: **Board** The board this field belongs to.
        cards: **Card** Cards under this field.

    """
    __tablename__ = 'field'

    id: Mapped[intpk] = mapped_column(init=False)
    board_id: Mapped[int] = mapped_column(ForeignKey('board.id'))
    name: Mapped[str] = mapped_column(String(50))
    board: Mapped['Board'] = relationship(back_populates='fields')
    cards: Mapped[List['Card']] = relationship(back_populates='field')
    archived: Mapped[bool] = mapped_column(default=False)
