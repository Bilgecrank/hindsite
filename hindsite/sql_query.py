"""
Central module for querying into the database.
"""
from sqlalchemy import select
from hindsite.db_setup import db
from hindsite.tables import User, Password


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


def is_user(email: str):
    """
    Returns if the user is actually a user in the database by checking if their
    email returns a result

    :param email: **str** Email to check against the database.
    :returns: **bool** Whether the user record is present in the database.
    """
    return get_user(email) is not None


def pass_valid(user_id: int, provided_hash: str):
    """
    Compares the password in the database to see if the supplied hash matches the stored hash.

    :param user_id: The user id of the record to be searched.
    :param provided_hash: The hash provided by the requester.
    :returns: **Bool** Whether the hash matches the hash stored in the database.
    """
    stmt = select(Password).filter_by(user_id=user_id).order_by(Password.password)
    stored_hash = db.session.execute(stmt).first()
    if stored_hash is not None:
        return provided_hash == stored_hash[0].password
    return False
