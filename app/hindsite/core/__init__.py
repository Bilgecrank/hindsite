"""
Core blueprints
"""

from flask import Blueprint

bp = Blueprint('auth', __name__)

# pylint: disable=wrong-import-position
from app.hindsite.core import core
# pylint: enable=wrong-import-position
