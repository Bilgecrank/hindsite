from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.hindsite.auth import auth