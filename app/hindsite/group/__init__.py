"""
Sets up the blueprint for home
"""
from flask import Blueprint

bp = Blueprint('home', __name__)

from app.hindsite.group import group
