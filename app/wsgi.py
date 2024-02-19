"""
App creation file
"""

from app.hindsite import create_app

app = create_app()

# pylint: disable=wrong-import-position
from app.test_data import populate_database
# pylint: enable=wrong-import-position

populate_database(app)
