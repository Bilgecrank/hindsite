"""
Test data function to populate the table with tables.
"""

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
        db.drop_all()
        db.create_all()

        register_user('emperorsgoodboi@imperium.vox',
                      'Iaintafraid_ofnuthin1')
        register_user('emperorsnotgoodboi@imperium.vox',
                      'Ialwaysaintafraid_ofnuthin1')
        register_user('emperorssortagoodboi@imperium.vox',
                      'Isometimesaintafraid_ofnuthin1')
        register_user('lancevancevt@gmail.com',
                      'Vht0326TST1!')
        register_user('emperors1goodboi@imperium.vox',
                      'Iaintafraid_ofnuthin1')
        register_user('emperors2notgoodboi@imperium.vox',
                      'Ialwaysaintafraid_ofnuthin1')
        register_user('emperor3ssortagoodboi@imperium.vox',
                      'Isometimesaintafraid_ofnuthin1')
        register_user('bemperorsgoodboi@imperium.vox',
                      'Iaintafraid_ofnuthin1')
        register_user('cemperorsnotgoodboi@imperium.vox',
                      'Ialwaysaintafraid_ofnuthin1')
        register_user('demperorssortagoodboi@imperium.vox',
                      'Isometimesaintafraid_ofnuthin1')

        group = create_group('Imperium', 'emperorsgoodboi@imperium.vox')

        board = core.create_board(group.id)
        core.create_board(group.id)
        core.create_board(group.id)
        field = core.add_field(board, 'A really good field.')
        core.add_field(board, "Another field")
        core.add_field(board, "An even better field")
        card = core.add_card(field, get_user('emperorsgoodboi@imperium.vox'), 'Test '
                                                                              'Test Test')
        core.add_card(field, get_user('emperorsgoodboi@imperium.vox'), 'Test '
                                                                       'Test Test Test')
        core.add_card(field, get_user('emperorsgoodboi@imperium.vox'), 'Test '
                                                                       'Test Test Test Test')
        print(card.message_body + "" + card.field.name + "" + str(card.field.board.start_time))
        output = ""
        for board in core.get_boards(group.id):
            output = output + str(board.id)
        output = output + "\n"
        for field in core.get_fields(board):
            output = output + str(field.name)
        output = output + "\n"
        print(output)
        print(core.get_fields(board))
        print(core.get_cards(field))
