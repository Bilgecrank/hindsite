"""
Defines logic flow for the authentication process.
"""
import re  # For serverside validation of secrets.

import bcrypt

from hindsite.db_setup import db
import hindsite.sql_query as query


def register_user(email: str, password: str):
    """
    Takes in a user's email and password, checks if the email is already associated with an account,
    then checks if the password is a valid entry.

    :param email:
    :param password:
    :return: **str** Returns a string indicating an error, or None if there is no error.
    """
    if not query.is_user(email):
        return 'ERROR: An account already exists with this email.'
    if not valid_secret(password):
        return ("Passwords must at least 12 characters long, include 1 uppercase letter, 1 lowercase letter, 1 number, "
                "and 1 special character (!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~).")
    hashword = bcrypt.hashpw(password.encode('utf-8'))
    # update.add_user(email, hashword)
    return None


def valid_secret(secret: str):
    """
    Checks if a supplied secret(e.g: password) meets minimum security requirements.

    :param secret: The supplied secret
    :return: **bool** Whether the secret meets the requirements.
    """
    if re.fullmatch(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!\"#$%&'()*+,-./:;<=>?@\[\]^"
                    r"_`{|}~]).{12,}", secret):
        return True
    return False
