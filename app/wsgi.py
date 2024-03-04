"""
App creation file
"""

from app.hindsite import create_app
from app.hindsite.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
