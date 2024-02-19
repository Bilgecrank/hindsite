"""
Defines logic adding and creating groups.
"""

from sqlalchemy import select
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


def get_groups(email: str):
    """
    Gets all group records belonging to a user.

    :param email: **str** Email to check against the database
    :returns: **list** A list of the user's current groups.
    """
    user = get_user(email)
    groups = []
    for membership in user.groups:
        if membership.invitation_accepted is True:
            groups.append(membership.group)
    return groups


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


def accept_invitation(membership: Membership):
    """
    Accepts an invitation to a group by setting the flag for <code>invitation_accepted</code>
     to True
    """
    membership.invitation_accepted = True
    db.session.commit()


def send_invitation(group_id: int, email: str):
    """
    Creates a Membership that signals an invitation to a user, by default the membership
    is not an ownership membership and will have <code>invitation_accepted</code> set to False

    :param group_id: The id of the group attached to the membership.
    :param email: The email of the user to be added to the membership.
    :returns: **Membership** A reference to the membership object.
    """
    user = get_user(email)
    group = get_group(group_id)
    membership = Membership(user, group)
    db.session.add(membership)
    db.session.commit()
    return membership


def get_group(group_id: int):
    """
    Gets a group record belonging to a user.

    :param group_id: **int** id to check against the database
    :returns: **group** or **None**
    """
    stmt = select(Group).where(Group.id == group_id)
    groups = db.session.execute(stmt).first()
    if groups is not None:
        return db.session.execute(stmt).first()[0]
    return None


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
