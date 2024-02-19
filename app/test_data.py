"""
Test data function to populate the table with tables.
"""

from app.hindsite.extensions import db
from app.hindsite.auth.authenticate_model import register_user

def populate_database(app):
    """
    Function that wipes and populates the database.
    :param app: Running flask app.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        register_user('emperorsgoodboi@imperium.vox', 'Iaintafraid_ofnuthin1')