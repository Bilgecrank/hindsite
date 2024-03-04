"""
Sets up the blueprint for home
"""
from flask import Blueprint

bp = Blueprint('home', __name__)

# pylint: disable=wrong-import-position
from app.hindsite.group import group
# pylint: enable=wrong-import-position
