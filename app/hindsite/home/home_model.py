"""
Defines logic adding and creating groups.
"""
from app.hindsite.extensions import db
from app.hindsite.common_model import get_user
from app.hindsite.tables import Group, Membership


class GroupAddError(Exception):
    """
    Definition for errors raised by the login function
    """

    message = None

    def __init__(self, message):
        self.message = message


def create_group(name: str, email: str):
    """
    Creates the group and associates the group with the current user. The creating
    user is labeled as the owner of the group.

    :param name: The name of the group to be created.
    :param email: The email of the user to be added to the group.
    :returns: **Group** The newly created group.
    """
    try:
        user = get_user(email)
        group = add_group(name)
        membership = Membership(user, group)
        membership.owner = True
        membership.invitation_accepted = True
        db.session.add(membership)
        db.session.commit()
    except GroupAddError as e:
        raise GroupAddError(e.message) from e
    return group


def add_group(name: str):
    """
    Inserts a group into the groups table of the database.
    need to take a user id and append the group id to the user record
    """
    if len(name) > 50:
        raise GroupAddError('Group name is too long(50 characters).')
    new_group = Group(name=name)
    db.session.add(new_group)
    db.session.commit()
    return new_group
