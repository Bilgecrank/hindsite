"""
    Common model to be used in submodels.
"""

from sqlalchemy import select

from app.hindsite.extensions import db
from app.hindsite.tables import User, Group


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

def get_all_users():
    """
    Gets all user records.

    :returns: **list** A list of all user records
    """
    stmt = select(User)
    users = db.session.execute(stmt).all()
    return users

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
