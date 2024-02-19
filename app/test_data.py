"""
Test data function to populate the table with tables.
"""

from app.hindsite.extensions import db
from app.hindsite.common_model import get_user
from app.hindsite.auth.authenticate_model import register_user
from app.hindsite.home.models import get_groups, create_group, send_invitation, accept_invitation, get_invitations
from app.hindsite.tables import Group, Membership


def populate_database(app):
    """
    Function that wipes and populates the database.
    :param app: Running flask app.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = [
            register_user('emperorsgoodboi@imperium.vox',
                        'Iaintafraid_ofnuthin1'),
            register_user('emperorsnotgoodboi@imperium.vox',
                          'Ialwaysaintafraid_ofnuthin1'),
            register_user('emperorssortagoodboi@imperium.vox',
                          'Isometimesaintafraid_ofnuthin1')
        ]
