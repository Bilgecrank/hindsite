"""
Association table for groups and users.
"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.hindsite import db


class Membership(db.Model):  # pylint: disable=too-few-public-methods
    """
    Associates user and groups.
    """
    __tablename__ = 'membership'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True,
                                         init=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('hindsite_group.id'), primary_key=True,
                                          init=False)
    user: Mapped['User'] = relationship(back_populates='groups')
    group: Mapped['Group'] = relationship(back_populates='users')
    owner: Mapped[bool] = mapped_column(default=False)
    invitation_accepted: Mapped[bool] = mapped_column(default=False)
