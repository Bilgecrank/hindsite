"""
Defines logic flow for the authentication process, additionally manages flask-login
session management.
"""

from sqlalchemy import select
from app.hindsite.extensions import db
from app.hindsite.tables import User, Group

class GroupAddError(Exception):
    """
    Definition for errors raised by the login function
    """

    message = None

    def __init__(self, message):
        self.message = message

def get_user(email: str):
    """
    Gets a single user record.

    :param email: **str** Email to check against the database
    :returns: **User** or **None**
    """
    stmt = select(User).filter_by(email=email)
    user = db.session.execute(stmt).first()
    if user is not None:
        return db.session.execute(stmt).first()[0]
    return None

def get_groups(email: str):
    """
    Gets all group records belonging to a user.

    :param email: **str** Email to check against the database
    :returns: **groups** or **None**
    """
    user = get_user(email)
    groups = user.groups
    return groups

def get_group(id: int):
    """
    Gets a group record belonging to a user.

    :param id: **int** id to check against the database
    :returns: **group** or **None**
    """
    stmt = select(Group).where(Group.id == id)
    groups = db.session.execute(stmt).first()
    if groups is not None:
        return db.session.execute(stmt).first()[0]
    return None

def create_group(name: str, email: str):
    """
    Creates the group and associates the group with the current user
    """
    user = get_user(email)
    group = add_group(name)
    user.groups.append(group)
    db.session.add(user)
    db.session.commit()
    return group


def add_group(name: str):
    """
    Inserts a group into the groups table of the database.
    need to take a user id and append the group id to the user record
    """
    new_group = Group(name=name)
    db.session.add(new_group)
    db.session.commit()
    return new_group
