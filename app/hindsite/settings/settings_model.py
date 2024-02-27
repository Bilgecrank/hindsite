"""
Settings Model.

This module provides the backend logic for handling user settings updates, including validating
inputs and updating the database.
"""

import bcrypt
from app.hindsite.extensions import db
from app.hindsite.common_model import get_user
from app.hindsite.tables import User
import re


class UpdateError(Exception):
    """
    Custom exception for update errors in user settings.
    """
    def __init__(self, message):
        self.message = message


def valid_email(email: str):
    """
      Validates entered emails that largely comply with RFC 5322:
      https://datatracker.ietf.org/doc/html/rfc5322#section-3.4

      :param email: **str** Email to be analyzed.

      :returns: **bool** Whether the email meats the requirements or not.
      """
    # Email validation pattern
    pattern = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*" \
              r"@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    return re.fullmatch(pattern, email)


def valid_display_name(display_name: str):
    """
    Validates a display name based on length and character set.

    Args:
        display_name (str): Display name to validate.

    Returns:
        bool: True if the display name is valid, False otherwise.
    """
    if not 2 <= len(display_name) <= 30:
        return False
    if not re.match(r'^[a-zA-Z0-9_\-]+$', display_name):
        return False
    if display_name != display_name.strip():
        return False
    return True


def valid_password(password: str):
    """
    Validates a password based on a regex pattern for security.

    Args:
        password (str): Password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    pattern = r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!\"#$%&'()*+,-./:;<=>?@\[\]^_`{|}~]).{12,}"
    return re.fullmatch(pattern, password)


def get_user_settings(email):
    """
        Retrieves user settings based on the user's email.

        Args:
            email (str): Email of the user.

        Returns:
            dict: A dictionary containing user settings if the user is found, None otherwise.
        """
    user = get_user(email)
    if user:
        return {'display_name': user.display_name, 'email': user.email}
    return None


def update_user_settings(email=User.email, new_display_name=None, new_email=None, new_password=None):
    """
        Updates user settings based on provided parameters.

        Args:
            email (str): Email of the user to update.
            new_display_name (str, optional): New display name for the user.
            new_email (str, optional): New email for the user.
            new_password (str, optional): New password for the user.

        Raises:
            UpdateError: If user is not found or input validation fails.
        """
    user = get_user(email)
    if not user:
        raise UpdateError("User not found.")

    if new_display_name and not valid_display_name(new_display_name):
        raise UpdateError("Invalid display name.")
    if new_email and not valid_email(new_email):
        raise UpdateError("Invalid email format.")
    if new_password and not valid_password(new_password):
        raise UpdateError("Invalid password format.")

        # if validations pass
    if new_display_name:
        user.display_name = new_display_name
    if new_email:
        user.email = new_email
    if new_password:
        user.password = new_password
        hashword = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        updated_user = User(password=Password(password=hashword), email=user.email,
                            display_name=user.display_name)
    db.session.commit()


def delete_account(email):
    """
        Deletes a user account from the database.

        Args:
            email (str): Email of the user whose account is to be deleted.

        Raises:
            Exception: If the user is not found in the database.

        Notes:
            This function is intended to be called from the Flask route that handles account deletion.
            The route should ensure that the user is authenticated and authorized to delete the account before calling this function.
        """
    user = get_user(email)  # Fetch the user by email
    if not user:
        raise Exception("User not found.")
    db.session.delete(user)  # Delete the user record
    db.session.commit()  # Commit the transaction
