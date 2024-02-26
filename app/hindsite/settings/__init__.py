"""
Sets up the blueprint for home
"""
from flask import Blueprint

bp = Blueprint('settings', __name__)

# pylint: disable=wrong-import-position
from app.hindsite.settings import settings
# pylint: enable=wrong-import-position
