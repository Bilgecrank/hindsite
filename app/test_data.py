"""
Test data function to populate the table with tables.
"""
from datetime import datetime

from app.hindsite.auth.authenticate_model import register_user
import app.hindsite.core.core_model as core
from app.hindsite.common_model import get_user

from app.hindsite.home.home_model import create_group
from app.hindsite.extensions import db


def populate_database(app):
    """
    Function that wipes and populates the database.
    :param app: Running flask app.
    """
    with app.app_context():
        # db.drop_all()
        db.create_all()
        # group = create_test_user_and_group()
        # create_test_bfcs(group)
        # tests_for_bfcs(group)
        # toggle_bfcs(group)
        # show_active_and_inactive_bfcs(group)


def create_test_user_and_group():
    """
    Populates the database with test users and a group.
    :return: **Group** The group created.
    """
    register_user('emperorsgoodboi@imperium.vox', 'emperorsgoodboi@imperium.vox',
                  'Iaintafraid_ofnuthin1', 'Iaintafraid_ofnuthin1')
    register_user('emperorsnotgoodboi@imperium.vox', 'emperorsnotgoodboi@imperium.vox',
                  'Ialwaysaintafraid_ofnuthin1', 'Ialwaysaintafraid_ofnuthin1')
    register_user('emperorssortagoodboi@imperium.vox', 'emperorssortagoodboi@imperium.vox',
                  'Isometimesaintafraid_ofnuthin1', 'Isometimesaintafraid_ofnuthin1')
    register_user('lancevancevt@gmail.com', 'lancevancevt@gmail.com',
                  'Vht0326TST1!', 'Vht0326TST1!')
    register_user('emperors1goodboi@imperium.vox', 'emperors1goodboi@imperium.vox',
                  'Iaintafraid_ofnuthin1', 'Iaintafraid_ofnuthin1')
    register_user('emperors2notgoodboi@imperium.vox', 'emperors2notgoodboi@imperium.vox',
                  'Ialwaysaintafraid_ofnuthin1', 'Ialwaysaintafraid_ofnuthin1')
    register_user('emperor3ssortagoodboi@imperium.vox', 'emperor3ssortagoodboi@imperium.vox',
                  'Isometimesaintafraid_ofnuthin1', 'Isometimesaintafraid_ofnuthin1')
    register_user('bemperorsgoodboi@imperium.vox', 'bemperorsgoodboi@imperium.vox',
                  'Iaintafraid_ofnuthin1', 'Iaintafraid_ofnuthin1')
    register_user('cemperorsnotgoodboi@imperium.vox', 'cemperorsnotgoodboi@imperium.vox',
                  'Ialwaysaintafraid_ofnuthin1', 'Ialwaysaintafraid_ofnuthin1')
    register_user('demperorssortagoodboi@imperium.vox', 'demperorssortagoodboi@imperium.vox',
                  'Isometimesaintafraid_ofnuthin1', 'Isometimesaintafraid_ofnuthin1')

    return create_group('Imperium', 'emperorsgoodboi@imperium.vox')


def create_test_bfcs(group):
    """
    Populates the database with boards-cards-fields
    :param group:
    :return:
    """
    board = core.create_board(group.id)
    core.create_board(group.id)
    core.create_board(group.id)
    field = core.add_field(board, 'A really good field.')
    core.add_field(board, 'A really good field.')
    core.add_field(board, 'A really good field.')
    core.add_card(field, get_user('emperorsgoodboi@imperium.vox'), 'Test '
                                                                   'Test Test')
    core.add_card(field, get_user('emperorsgoodboi@imperium.vox'), 'Test '
                                                                   'Test Test Test')
    core.add_card(field, get_user('emperorsgoodboi@imperium.vox'), 'Test ')


def tests_for_bfcs(group):
    """
    Generic tests for board-field-cards
    :param group:
    :param board:
    :param field:
    :return:
    """
    board = group.boards[0]
    field = board.fields[1]  # Second field
    card = board.fields[0].cards[1]  # Second card of first field.
    print(str(board.end_time))
    core.set_end_date_for_board(board, datetime.now())
    print(str(board.end_time))
    output = ''
    core.move_card(card, field)
    for a_card in core.get_cards(field):
        output = output + a_card.message_body
    print(output)


def toggle_bfcs(group):
    """
    Tests all the toggle functions
    :param group:
    :param board:
    :param field:
    :return:
    """
    boards = core.get_boards(group.id)
    fields = core.get_fields(boards[0])
    cards = core.get_cards(fields[0])
    core.toggle_archive_board(boards[2])
    core.toggle_archive_field(fields[2])
    core.toggle_archive_card(cards[1])


def show_active_and_inactive_bfcs(group):
    """
    Shows active and inactive board-card-fields
    :param group:
    :param board:
    :param field:
    :return:
    """
    output = ''
    print('Active Entities')
    for got_board in core.get_boards(group.id):
        output = output + str(got_board.id) + ' | '
    output = output + '\n'
    for got_field in core.get_fields(group.boards[0]):
        output = output + got_field.name + ' | '
    output = output + '\n'
    for got_card in core.get_cards(group.boards[0].fields[0]):
        output = output + got_card.message_body + ' | '
    print(output)
    print('Inactive Entities')
    output = ''
    for got_board in core.get_boards(group.id, True):
        output = output + str(got_board.id) + ' | '
    output = output + '\n'
    for got_field in core.get_fields(group.boards[0], True):
        output = output + got_field.name + ' | '
    output = output + '\n'
    for got_card in core.get_cards(group.boards[0].fields[0], True):
        output = output + got_card.message_body + ' | '
    print(output)
