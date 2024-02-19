"""
Class definition for the group table
"""
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.hindsite.extensions import db, intpk


class Group(db.Model):  # pylint: disable=too-few-public-methods
    """
    Defines a group identifier and attaches a name to that group

    Attributes:
        id: **int** Primary key id for table, initialized automatically
        name: **str** Identifying name for the group.

    """
    __tablename__ = 'hindsite_group'

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50))
    users: Mapped[List['UserMembership']] = relationship(back_populates='group', init=False)
    boards = relationship('Board', back_populates='groups')
