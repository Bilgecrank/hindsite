"""
Defines logic adding and creating groups.
"""

from sqlalchemy import select
from app.hindsite.extensions import db
from app.hindsite.common_model import get_group, get_user
from app.hindsite.tables import Group, Membership


class GroupAddError(Exception):
    """
    Definition for errors raised by the login function
    """

    message = None

    def __init__(self, message):
        self.message = message



def get_invitations(email: str):
    """
    Looks at memberships matching the user with the supplied email and
    returns all invitations that are currently active.

    :param email: Email of the user being checked for invitations.
    :returns: **List** A list of Memberships for invitations.
    """
    user = get_user(email)
    invitations = []
    for membership in user.groups:
        if membership.invitation_accepted is False:
            invitations.append(membership)
    return invitations


def get_invitation(group_id: int, email: str):
    """
    Looks at memberships matching the user with the supplied email and
    returns all invitations that are currently active.

    :param group_id: ID of the group to get the invitation of
    :param email: Email of the user being checked for invitations.
    :returns: **List** A list of Memberships for invitations.
    """
    invitations = get_invitations(email)
    membership = None
    for invitation in invitations:
        if int(invitation.group.id) == int(group_id):
            membership = invitation
    return membership


def accept_invitation(membership: Membership):
    """
    Accepts an invitation to a group by setting the flag for <code>invitation_accepted</code>
     to True
    """
    membership.invitation_accepted = True
    db.session.commit()


def create_group(name: str, email: str):
    """
    Creates the group and associates the group with the current user. The creating
    user is labeled as the owner of the group.

    :param name: The name of the group to be created.
    :param email: The email of the user to be added to the group.
    :returns: **Group** The newly created group.
    """
    user = get_user(email)
    group = add_group(name)
    membership = Membership(user, group)
    membership.owner = True
    membership.invitation_accepted = True
    db.session.add(membership)
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
