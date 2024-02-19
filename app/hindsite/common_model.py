"""
    Common model to be used in submodels.
"""

from sqlalchemy import select

from app.hindsite.extensions import db
from app.hindsite.tables import User

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
