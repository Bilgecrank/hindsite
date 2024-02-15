"""
Blueprint for group page view
"""

from flask import Blueprint

bp = Blueprint('group', __name__)

# pylint: disable=wrong-import-position
from app.hindsite.group_page import group_page
# pylint: enable=wrong-import-position
