"""
This  module defines all logic essential to updating and creating information in the database.
"""

from app.hindsite.tables.base import db
from app.hindsite.tables import User, Password


def add_user(user_info: dict):
    """
    Inserts a user into the database.

    :param user_info: **dict** User info containing `'display_name'`, `'email'`,
    and `'password'`. The password should already be hashed.
    :raises exc.IntegrityError: Raises if there's an issue inserting the user.
    """
    new_user = User(display_name=user_info['display_name'],
                    email=user_info['email'])
    new_user_pass = Password(user_id=new_user,
                             password=user_info['password'])
    new_user.password = [new_user_pass]
    db.session.add(new_user)
    db.session.commit()
    return new_user

