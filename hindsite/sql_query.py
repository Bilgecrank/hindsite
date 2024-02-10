"""
Central module for querying into the database.
"""
from sqlalchemy import select
from hindsite.db_setup import db
from hindsite.tables import User, Password


class QueryError(Exception):
    """
    Defines an issue that arises with a query.
    """


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


def get_hashword(user_id: int):
    """
    Compares the password in the database to see if the supplied hash matches the stored hash.

    :param user_id: The user id of the record to be searched.
    :returns: **PyBytes** Returns an encoding password to be matched.

    :raises QueryError: Raises when a password record is not found for a user.
    """
    stmt = select(Password).filter_by(user_id=user_id).order_by(Password.password)
    password_record = db.session.execute(stmt).first()
    if password_record is None:
        raise QueryError('A password was not found!')
    return password_record[0].password.encode('utf-8')
