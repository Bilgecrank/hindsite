"""
Contains the model for defining the Board table in the database.
"""
import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.hindsite.extensions import db, intpk


class Board(db.Model):  # pylint: disable=too-few-public-methods
    """
    The Board table acts as an aggregate to fields.
    """
    __tablename__ = 'board'

    id: Mapped[intpk] = mapped_column(init=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('group.id'))
    archived: Mapped[bool] = mapped_column(default=False)
    timer = mapped_column(DateTime(timezone=True))

    start_time = mapped_column(DateTime(timezone=True),
                               default=datetime.datetime.now())
    end_time = mapped_column(DateTime(timezone=True))
    groups = relationship('Group', back_populates='boards')
