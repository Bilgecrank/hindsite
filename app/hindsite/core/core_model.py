"""
Defines retrospective models to access boards, fields and cards.
"""
import datetime

from sqlalchemy.orm import Mapped

from app.hindsite import db
from app.hindsite.common_model import get_group
from app.hindsite.tables import Board, Field, Card


class BoardError(Exception):
    """
    Definition for errors raised by board function
    """

    message = None

    def __init__(self, message):
        self.message = message


class FieldError(Exception):
    """
    Definition for errors raised by field functions
    """

    message = None

    def __init__(self, message):
        self.message = message


class CardError(Exception):
    """
    Definition for errors raised by card functions
    """

    message = None

    def __init__(self, message):
        self.message = message


def create_board(group_id: int):
    """
    Creates a board and matches it to a group_id.

    :param group_id:
    :return: The Board object created.
    """
    new_board = Board(get_group(group_id))
    db.session.add(new_board)
    db.session.commit()
    return new_board


def add_field(board: Board, name: str):
    """
    Adds a field to an existing board.

    :param board: **Board** The board object the field will be attached to.
    :param name: **str** The plaintext name of the field.
    :return: **Field** The field object committed into the database.
    """
    if len(name) > 50:
        raise FieldError("Field name too long(50 characters).")
    new_field = Field(board, name)
    db.session.commit()
    return new_field


def add_card(field: Field, author, card_body: str):
    """
    Adds a new card to a field.

    :param field: **Field** Target field the card is being added to.
    :param author: **User** User object that created the card.
    :param card_body: **str** The initial message the card will read.
    :return: **Card** The card object committed in the database.
    """
    if len(card_body) > 2000:
        raise CardError("Card message is too long(2000 characters).")
    new_card = Card(field, author, card_body)
    db.session.commit()
    return new_card


def set_end_date_for_board(board: Board, end_date_time: datetime.datetime):
    """
    Sets a new end date for the board.

    :param board: **Board** The board to be modified.
    :param end_date_time:
    :return:
    """
    if end_date_time > board.start_time:
        raise BoardError("End time is before start time.")
    board.end_time = end_date_time
    db.session.commit()
    return board


def update_field(field: Field, name: str):
    """
    Updates the name of a field.

    :param field: **Field** The field object to be updated.
    :param name: **str** The new name of the field.
    :return: **Field** The updated field.
    """
    if len(name) > 50:
        raise FieldError("Field name too long(50 characters).")
    field.name = name
    db.session.commit()
    return field
