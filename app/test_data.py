"""
Test data function to populate the table with tables.
"""

from app.hindsite.extensions import db


def populate_database(app):
    """
    Function that wipes and populates the database.
    :param app: Running flask app.
    """
    with app.app_context():
        #db.drop_all()
        db.create_all()

        # register_user('emperorsgoodboi@imperium.vox',
        #             'Iaintafraid_ofnuthin1')
        # register_user('emperorsnotgoodboi@imperium.vox',
        #               'Ialwaysaintafraid_ofnuthin1')
        # register_user('emperorssortagoodboi@imperium.vox',
        #               'Isometimesaintafraid_ofnuthin1')
        # register_user('lancevancevt@gmail.com',
        #               'Vht0326TST1!')
        # register_user('emperors1goodboi@imperium.vox',
        #             'Iaintafraid_ofnuthin1')
        # register_user('emperors2notgoodboi@imperium.vox',
        #               'Ialwaysaintafraid_ofnuthin1')
        # register_user('emperor3ssortagoodboi@imperium.vox',
        #               'Isometimesaintafraid_ofnuthin1')
        # register_user('bemperorsgoodboi@imperium.vox',
        #             'Iaintafraid_ofnuthin1')
        # register_user('cemperorsnotgoodboi@imperium.vox',
        #               'Ialwaysaintafraid_ofnuthin1')
        # register_user('demperorssortagoodboi@imperium.vox',
        #               'Isometimesaintafraid_ofnuthin1')
