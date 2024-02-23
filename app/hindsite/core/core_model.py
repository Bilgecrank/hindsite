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

# CREATE

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


def add_card(field: Field, author: 'User', card_message: str):
    """
    Adds a new card to a field.

    :param field: **Field** Target field the card is being added to.
    :param author: **User** User object that created the card.
    :param card_message: **str** The initial message the card will read.
    :return: **Card** The card object committed in the database.
    """
    if len(card_message) > 2000:
        raise CardError("Card message is too long(2000 characters).")
    new_card = Card(field, author, card_message)
    db.session.commit()
    return new_card


# READ


def get_boards(group_id: int):
    """
    Retrieves a list of references to the boards attached to a group.

    :param group_id: **int** The primary key of the group.
    :return: **List[Board]** The boards attached to the group.
    """
    group = get_group(group_id)
    return group.boards


def get_fields(board: Board):
    """
    Returns a list of fields attached to a board.

    :param board: **Board** The selected board to derive fields from.
    :return: **List[Field]** A list of fields associated with the board.
    """
    return board.fields


def get_cards(field: Field):
    """
    Returns a list of cards attached to a field.

    :param field: **Field** The selected field to derive cards from.
    :return: **List[Card]** A list of cards associated with the field.
    """
    return field.cards


# UPDATE


def set_end_date_for_board(board: Board, end_date_time: datetime.datetime):
    """
    Sets a new end date for the board.

    :param board: **Board** The board to be modified.
    :param end_date_time: **datetime** The end date-time of the board.
    :return: **Board** The board that was modified.
    """
    if end_date_time > board.start_time:
        raise BoardError("End time is before start time.")
    board.end_time = end_date_time
    db.session.commit()
    return board

def update_field_name(field: Field, name: str):
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

def move_card(card: Card, field: Field):
    """
    Changes the assigned field of a card from the current to the one specified.

    :param card: **Card** The card to be moved.
    :param field: **Field** The field the card will be moved to.
    :return: **Card** The card that was moved.
    """
    card.field = field
    db.session.commit()
    return card

def update_card_message(card: Card, card_message: str):
    """
    Updates the message on the card to a new value.

    :param card: **Card** The card to be updated.
    :param card_message: **str** The new or edited message.
    :return: **Card** The updated card.
    """
    if len(card_message) > 2000:
        raise CardError("Card message is too long(2000 characters).")
    card.message_body = card_message
    db.session.commit()
    return card

def update_card_owner(card: Card, new_owner: 'User'):
    """
    Updates the owner of a card indicating possession of an issue or retrospective.

    :param card: **Card** The card to be updated.
    :param new_owner: **User** The user being assigned to the card.
    :return: **Card** The card that was updated.
    """
    card.owner = new_owner
    db.session.commit()
    return card

def update_card_status(card: Card, new_status: str):
    """
    Changes the status of a card.

    :param card: **Card** The card to be updated.
    :param new_status: **str** The new status being assigned to the card.
    :return: **Card** The card that was updated.
    """
    if len(new_status) > 50:
        raise CardError("The status message is too long(50 characters).")
    card.card_status = new_status
    db.session.commit()
    return card
