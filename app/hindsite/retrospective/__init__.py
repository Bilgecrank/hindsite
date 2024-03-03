"""
Core blueprints
"""

from flask import Blueprint

bp = Blueprint('retrospective', __name__)

# pylint: disable=wrong-import-position
from app.hindsite.history import history
# pylint: enable=wrong-import-position
