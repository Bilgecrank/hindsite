from flask import Blueprint

bp = Blueprint('home', __name__)

from app.hindsite.home import home