"""
Allows the user to search for other users and send invites, while displaying user cards
for all users who belong to the current group.
"""

from sqlalchemy import select

from app.hindsite.extensions import db
from app.hindsite.tables import User

class UserSearchError(Exception):
    """
    Definition for errors raised by the login function
    """

    message = None

    def __init__(self, message):
        self.message = message

def get_users(term: str):
    """
    Gets a single user record.

    :param email: **str** Email to check against the database
    :returns: **User** or **None**
    """
    if term is not None:
        users = db.session.query(User).where(User.email.contains(term))
        if users is not None:
            return users
        return None