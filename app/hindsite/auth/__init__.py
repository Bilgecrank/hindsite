"""
Blueprint for authenticate views
"""

from flask import Blueprint

bp = Blueprint('auth', __name__)

# pylint: disable=wrong-import-position
from app.hindsite.auth import auth
# pylint: enable=wrong-import-position
