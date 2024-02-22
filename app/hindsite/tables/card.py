"""
Defines the model for the cards and their relationships to others tables in the database.
"""

from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.hindsite.extensions import db, intpk


class Card(db.Model):  # pylint: disable=too-few-public-methods
    """
    The Card holds comments and reactions from other users in the application.
    Attributes:
        id: **int** Primary key for the card
        field_id: **int** Foreign key referencing the field this card belongs to
        author_id: **int** Foreign key referencing the user who created the card
        owner_id: **int** Foreign key (optional) referencing the user who is
        charged with the issue/content of the card.
        message_body: **str** The body of the content in the card.
        archived: **bool** Whether the card has been 'deleted'.
        field: **Field** Field that the card belongs to.
        author: **User** Author of the card.
        owner: **User** Assigned owner of the issue/subject in the card.


    """
    __tablename__ = 'card'

    id: Mapped[intpk] = mapped_column(init=False)
    field_id: Mapped[int] = mapped_column(ForeignKey('field.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user.id'))
    message_body: Mapped[str] = mapped_column(String(2000))
    card_status: Mapped[str] = mapped_column(String(50))
    field: Mapped['Field'] = relationship(back_populates='cards')
    author: Mapped['User'] = relationship(foreign_keys=[author_id])
    owner: Mapped['User'] = relationship(foreign_keys=[owner_id])
    archived: Mapped[bool] = mapped_column(default=False)
