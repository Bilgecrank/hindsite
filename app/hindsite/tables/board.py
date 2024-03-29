"""
Contains the model for defining the Board table in the database.
"""
import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.hindsite.extensions import db, intpk


class Board(db.Model):  # pylint: disable=too-few-public-methods
    """
    The Board table acts as an aggregate to fields.
    Attributes:
        id: **int** Primary key for the board
        group_id: **int** Foreign key referencing the group the board belongs to.
        timer: **datetime** Target time that timer is counting down to.
        end_time: **datetime** Time the board's retrospective ended.
        start_time: **datetime** Time the board's restrospective started.
        archived: **bool** Whether the board is 'deleted'.
        groups: **Group** The group the board belongs to.
        fields: **Field** Fields under this board.

    """
    __tablename__ = 'board'

    id: Mapped[intpk]
    group_id: Mapped[int] = mapped_column(ForeignKey('hindsite_group.id'))
    timer: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    group: Mapped['Group'] = relationship(back_populates='boards')
    fields: Mapped[List['Field']] = relationship(back_populates='board')
    archived: Mapped[bool] = mapped_column(default=False)

    def __init__(self, group, start_time, end_time ):
        self.group = group
        self.start_time = start_time
        self.end_time = end_time
