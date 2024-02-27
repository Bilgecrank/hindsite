"""
Test data function to populate the table with tables.
"""
from datetime import datetime

from app.hindsite.auth.authenticate_model import register_user
import app.hindsite.common_model as core
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

        # register_user('emperorsgoodboi@imperium.vox','emperorsgoodboi@imperium.vox',
        #               'Iaintafraid_ofnuthin1','Iaintafraid_ofnuthin1')
        # register_user('emperorsnotgoodboi@imperium.vox','emperorsnotgoodboi@imperium.vox',
        #               'Ialwaysaintafraid_ofnuthin1','Ialwaysaintafraid_ofnuthin1')
        # register_user('emperorssortagoodboi@imperium.vox','emperorssortagoodboi@imperium.vox',
        #               'Isometimesaintafraid_ofnuthin1','Isometimesaintafraid_ofnuthin1')
        # register_user('lancevancevt@gmail.com','lancevancevt@gmail.com',
        #               'Vht0326TST1!','Vht0326TST1!')
        # register_user('emperors1goodboi@imperium.vox','emperors1goodboi@imperium.vox',
        #               'Iaintafraid_ofnuthin1','Iaintafraid_ofnuthin1')
        # register_user('emperors2notgoodboi@imperium.vox','emperors2notgoodboi@imperium.vox',
        #               'Ialwaysaintafraid_ofnuthin1','Ialwaysaintafraid_ofnuthin1')
        # register_user('emperor3ssortagoodboi@imperium.vox','emperor3ssortagoodboi@imperium.vox',
        #               'Isometimesaintafraid_ofnuthin1','Isometimesaintafraid_ofnuthin1')
        # register_user('bemperorsgoodboi@imperium.vox','bemperorsgoodboi@imperium.vox',
        #               'Iaintafraid_ofnuthin1','Iaintafraid_ofnuthin1')
        # register_user('cemperorsnotgoodboi@imperium.vox','cemperorsnotgoodboi@imperium.vox',
        #               'Ialwaysaintafraid_ofnuthin1','Ialwaysaintafraid_ofnuthin1')
        # register_user('demperorssortagoodboi@imperium.vox','demperorssortagoodboi@imperium.vox',
        #               'Isometimesaintafraid_ofnuthin1','Isometimesaintafraid_ofnuthin1')

        # group = create_group('Imperium', 'emperorsgoodboi@imperium.vox')

        # board = core.create_board(group.id)
        # core.create_board(group.id)
        # core.create_board(group.id)
        # field = core.add_field(board, 'A really good field.')
        # field2 = core.add_field(board, 'A really good field.')
        # core.add_field(board, 'A really good field.')
        # card = core.add_card(field, get_user('emperorsgoodboi@imperium.vox'), 'Test '
        #                                                                       'Test Test')
        # card2 = core.add_card(field, get_user('emperorsgoodboi@imperium.vox'), 'Test '
        #                                                                'Test Test Test')
        # core.add_card(field, get_user('emperorsgoodboi@imperium.vox'), 'Test ')
        # print(str(board.end_time))
        # core.set_end_date_for_board(board, datetime.now())
        # print(str(board.end_time))
        # output = ''
        # core.move_card(card2, field2)
        # for a_card in core.get_cards(field2):
        #     output = output + a_card.message_body
        # print(output)
        # output = ''
        # for got_board in core.get_boards(group.id):
        #     output = output + str(got_board.id) + ' | '
        # output = output + '\n'
        # for got_field in core.get_fields(board):
        #     output = output + got_field.name + ' | '
        # output = output + '\n'
        # for got_card in core.get_cards(field):
        #     output = output + got_card.message_body + ' | '

        # print(output)
