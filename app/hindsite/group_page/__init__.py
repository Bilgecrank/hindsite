from flask import Blueprint

bp = Blueprint('group', __name__)

from app.hindsite.group_page import group_page