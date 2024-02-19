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
        #TODO: Change this to filter_by with an | clause in between
        users = db.session.query(User) \
        .filter(User.display_name.icontains(term) \
                | User.email.icontains(term) \
                | User.first_name.icontains(term) \
                | User.last_name.icontains(term))
        if users is not None:
            return users
        return None