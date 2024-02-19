"""
Sets up the blueprint for home
"""
from flask import Blueprint

bp = Blueprint('home', __name__)

# pylint: disable=wrong-import-position
from app.hindsite.home import home
# pylint: enable=wrong-import-position
