"""
Test data function to populate the table with tables.
"""

from app.hindsite.extensions import db
from app.hindsite.common_model import get_user
from app.hindsite.auth.authenticate_model import register_user
from app.hindsite.tables import Group, Membership


def populate_database(app):
    """
    Function that wipes and populates the database.
    :param app: Running flask app.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        register_user('emperorsgoodboi@imperium.vox', 'Iaintafraid_ofnuthin1')
        new_group = Group('Imperium')
        membership = Membership()
        user = get_user('emperorsgoodboi@imperium.vox')
        membership.user = user
        membership.owner = True
        new_group.users.append(membership)
        db.session.add(new_group)
        db.session.commit()
        print([membership.user.email, membership.group.name])
