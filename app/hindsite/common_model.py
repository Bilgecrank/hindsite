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
