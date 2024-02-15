from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.hindsite.core import core