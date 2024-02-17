"""
App creation
"""
from sqlalchemy import select

from app.hindsite import create_app
from app.hindsite.extensions import db
app = create_app()

from app.hindsite.tables import *
# TEST OPTION: WIPE DATA FROM DB.
with app.app_context():
    db.drop_all()
    db.create_all()

