"""
    Common model to be used in submodels.
"""
import datetime
from typing import Callable
from flask import session
from sqlalchemy import select

from app.hindsite.extensions import db
from app.hindsite.tables import User, Group
from app.hindsite.tables.board import Board
from app.hindsite.tables.card import Card
from app.hindsite.tables.field import Field


def get_user(email: str):
    """
    Gets a single user record.

    :param email: **str** Email to check against the database
    :returns: **User** or **None**
    """
    stmt = select(User).filter_by(email=email)
    user = db.session.execute(stmt).first()
    if user is not None:
        return db.session.execute(stmt).first()[0]
    return None


def get_all_users():
    """
    Gets all user records.

    :returns: **list** A list of all user records
    """
    stmt = select(User)
    users = db.session.execute(stmt).all()
    return users


def get_groups(email: str):
    """
    Gets all group records belonging to a user.

    :param email: **str** Email to check against the database
    :returns: **list** A list of the user's current groups.
    """
    user = get_user(email)
    groups = []
    for membership in user.groups:
        if membership.invitation_accepted is True:
            groups.append(membership.group)
    return groups

def get_ownership(email: str, group_id: int):
    """
    Checks for group ownership

    :param email: **str** Email to find the user
    :param group_id: **int** Group id to check for ownership in
    :returns: **bool** True or False
    """
    user = get_user(email)
    groups = []
    ownership = False
    for membership in user.groups:
        if membership.owner is True:
            groups.append(membership.group)
    for group in groups:
        if group.id == group_id:
            ownership = True
    return ownership

def get_group(group_id: int):
    """
    Gets a group record belonging to a user.

    :param group_id: **int** id to check against the database
    :returns: **group** or **None**
    """
    stmt = select(Group).where(Group.id == group_id)
    groups = db.session.execute(stmt).first()
    if groups is not None:
        return db.session.execute(stmt).first()[0]
    return None

def authorized_routes(route_1: Callable, route_2: Callable):
    """
    Calls routes based on the value of the facilitator session variable

    :route_1: **Callable** route to call if true
    :route_2: **Callable** route to call if false

    :returns: **Callable** returns the selected route
    """
    facilitator = False
    if 'facilitator' in session:
        facilitator = session.get('facilitator')
    if facilitator is True:
        return route_1
    return route_2

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


def create_board(group_id: int,
                 start_time: datetime = datetime.datetime.now(),
                 end_time: datetime = datetime.datetime.now() +
                                      datetime.timedelta(30)):
    """
    Creates a board and matches it to a group_id.

    :param group_id:
    :param start_time:
    :param end_time:

    :return: The Board object created.
    """
    new_board = Board(get_group(group_id), start_time, end_time)
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
    db.session.add(new_field)
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
    db.session.add(new_card)
    db.session.commit()
    return new_card


# READ

def get_board(group_id: int, board_id: int):
    """
    Retrieves the most recent board attached to a group

    :param group_id: **int** The primary key of the group.
    :param archive_status: **bool** Whether to get active boards(false) or archived boards(true).
    :return: **board** The board attached to the group with the id or **None**.
    """
    group = get_group(group_id)
    rtn_board = None
    for board in group.boards:
        if board.archived is False:
            if board.id == board_id:
                rtn_board = board
    return rtn_board


def get_boards(group_id: int, archive_status=False):
    """
    Retrieves a list of references to the boards attached to a group.

    :param group_id: **int** The primary key of the group.
    :param archive_status: **bool** Whether to get active boards(false) or archived boards(true).
    :return: **List[Board]** The boards attached to the group.
    """
    group = get_group(group_id)
    board_list = []
    for board in group.boards:
        if board.archived is archive_status:
            board_list.append(board)
    return board_list


def get_all_boards_by_end_date(group_id: int):
    """
    Returns a list of boards by end_date descending.
    :param group_id: The id of the group associated with the boards.
    :return: **List** of **Board** with end-date descending.
    """
    group = get_group(group_id)
    stmt = select(Board).where(Board.group == group).order_by(Board.end_time.desc())
    return db.session.execute(stmt).all()


def get_fields(board: Board, archive_status=False):
    """
    Returns a list of fields attached to a board.

    :param board: **Board** The selected board to derive fields from.
    :param archive_status: **bool** Whether to get active fields(false) or archived fields(true).
    :return: **List[Field]** A list of fields associated with the board.
    """
    field_list = []
    for field in board.fields:
        if field.archived is archive_status:
            field_list.append(field)
    return field_list

def get_field(field_id: int, board: Board):
    """
    Returns a single field attached to a board.

    :param board: **Board** The selected board to derive the field from.
    :param field_id: **int** The id of the field to select
    :return: **Field** The selected field or **None** if the field isn't found
    """
    rtn_field = None
    for field in board.fields:
        if field.archived is False:
            if field.id == field_id:
                rtn_field = field
    return rtn_field

def get_cards(field: Field, archive_status=False):
    """
    Returns a list of cards attached to a field.

    :param field: **Field** The selected field to derive cards from.
    :param archive_status: **bool** Whether to get active cards(false) or archived cards(true).
    :return: **List[Card]** A list of cards associated with the field.
    """
    card_list = []
    for card in field.cards:
        if card.archived is archive_status:
            card_list.append(card)
    return card_list

def get_card(card_id: int, field: Field):
    """
    Returns a single card based on the card_id and field
    """
    rtn_card = None
    for card in field.cards:
        if card.archived is False:
            if card.id == card_id:
                rtn_card = card
    return rtn_card
# UPDATE


def set_start_date_for_board(board: Board, start_date_time: datetime.datetime):
    """
    Sets a new start date for the board.

    :param board: **Board** The board to be modified.
    :param end_date_time: **datetime** The start date-time of the board.
    :return: **Board** The board that was modified.
    """
    if start_date_time < datetime.datetime.today():
        raise BoardError("Start time is before current time and date")
    board.start_time = start_date_time
    db.session.commit()
    return board


def set_end_date_for_board(board: Board, end_date_time: datetime.datetime):
    """
    Sets a new end date for the board.

    :param board: **Board** The board to be modified.
    :param end_date_time: **datetime** The end date-time of the board.
    :return: **Board** The board that was modified.
    """
    if end_date_time < board.start_time:
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


# DELETE


def toggle_archive_board(board: Board):
    """
    Toggles the archive status of a board.

    :param board: The board to be archived or reactivated.
    :return: The board whose archival was changed.
    """
    board.archived = not board.archived
    db.session.commit()
    return board


def toggle_archive_field(field: Field):
    """
    Toggles the archive status of a field.

    :param field: **Field** The field to be archived or reactivated.
    :return: **Field** The field whose archival was changed.
    """
    field.archived = not field.archived
    db.session.commit()
    return field

def toggle_archive_card(card: Card):
    """
    Toggles the archive status of a card
    :param card: **Card** The card to be archived or reactivated.
    :return: **Card** The card whose archival was changed.
    """
    card.archived = not card.archived
    db.session.commit()
    return card
