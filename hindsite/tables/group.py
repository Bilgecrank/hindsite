"""
Class definition for the group table
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from hindsite.db_setup import db, intpk, user_membership


class Group(db.Model):
    """
    Defines a group identifier and attaches a name to that group

    Attributes:
        id: **int** Primary key id for table, initialized automatically
        name: **str** Identifying name for the group.

    """
    __tablename__ = 'group'

    id: Mapped[intpk] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50))
    users = relationship('User', secondary=user_membership, back_populates='groups')
