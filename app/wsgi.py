"""
App creation file
"""

from app.hindsite import create_app

app = create_app()

from app.test_data import populate_database

populate_database(app)
