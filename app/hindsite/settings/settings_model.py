"""
Settings Model.

This module provides the backend logic for handling user settings updates, including validating
inputs and updating the database.
"""

import bcrypt

from app.hindsite.auth.authenticate_model import valid_email, valid_secret, valid_display_name
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


def update_user_settings(user: 'User',
                         new_display_name=None,
                         new_email=None,
                         new_password=None):
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
    if not user:
        raise UpdateError("User not found.")

    if new_display_name:
        if not valid_display_name(new_display_name):
            raise UpdateError("Invalid display name.")
        user.display_name = new_display_name
    if new_email:
        if not valid_email(new_email):
            raise UpdateError("Invalid email format.")
        user.email = new_email
    if new_password:
        if not valid_secret(new_password):
            raise UpdateError("Invalid password format.")
        hashword = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user.password.password = hashword

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
