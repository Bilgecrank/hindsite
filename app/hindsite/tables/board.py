"""
Contains the model for defining the Board table in the database.
"""
import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.hindsite.tables.base import db, intpk


class Board(db.Model):  # pylint: disable=too-few-public-methods
    """
    The Board table acts as an aggregate to fields.
    """
    __tablename__ = 'board'

    id: Mapped[intpk] = mapped_column(init=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('hs_group.id'))

    timer: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    end_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                          default=datetime.datetime.now())
    archived: Mapped[bool] = mapped_column(default=False)
    groups = relationship('Group', back_populates='boards')
    fields = relationship('Field', back_populates='board')
