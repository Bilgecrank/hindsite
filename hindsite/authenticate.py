"""
Defines logic flow for the authentication process.
"""
import re  # For serverside validation of secrets.

import bcrypt
import hindsite.sql_query as query


class RegisterError(Exception):
    """
    Definition for errors raised by the register_user function
    """


class LoginError(Exception):
    """
    Definition for errors raised by the login function
    """


def register_user(email: str, password: str):
    """
    Takes in a user's email and password, checks if the email is already associated with an account,
    then checks if the password is a valid entry.

    :param email:
    :param password:
    :return: **str** Returns a string indicating an error, or None if there is no error.

    :raises RegisterError: Raises this in case of an already extant account or if the password is
     not a valid secret.
    """
    if query.is_user(email):
        raise RegisterError('ERROR: An account already exists with this email.')
    if not valid_secret(password):
        raise RegisterError(
            'Passwords must at least 12 characters long, include 1 uppercase letter, 1 lowercase '
            'letter, 1 number, and 1 special character (!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~).')
    hashword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # update.add_user(email, hashword)
    return True


def valid_secret(secret: str):
    """
    Checks if a supplied secret(e.g: password) meets minimum security requirements.

    :param secret: The supplied secret
    :return: **bool** Whether the secret meets the requirements.
    """
    return re.fullmatch(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!\"#$%&'()*+,-./:;<=>?@\[\]^"
                        r"_`{|}~]).{12,}", secret)


def login(email: str, password: str):
    """
    Logs a user into the system, initializing a session.

    :param email: **str** The email of the login request.
    :param password: **str** An unhashed password that should match the account its attached to.
    :return: **str** Returns a string indicating an error or **None** if login was successful.
    """
    if not query.is_user(email):
        raise LoginError('This email is not attached to an account.')
    user_id = query.get_user(email).id
    if bcrypt.checkpw(password.encode('utf-8'), query.get_hashword(user_id)):
        return True
    return False
