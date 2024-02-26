"""

"""
from flask_login import current_user
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


def update_user_settings(new_display_name=None, new_email=None, new_password=None):
    user = current_user
    if user:
        if new_display_name:
            User.display_name = new_display_name
        if new_email:
            User.email = new_email
        if new_password:
            User.password = new_password
        try:
            db.session.commit()
            return new_password, new_email, new_display_name
        except Exception as e:
            db.session.rollback()
            # Log the exception e
            return False
    else:
        return False

def update_user_display_name(user_id, new_display_name):
    print(f"Entering update_user_display_name with user_id: {user_id} and new_display_name: {new_display_name}")  # Debug print at function start

    # Fetch the user by ID
    user = User.query.get(user_id)

    if user:
        print(f"User found: {user.id}. Updating display name to: {new_display_name}")  # Debug print before updating
        # Update the user's display name
        user.display_name = new_display_name

        # Commit the changes to the database
        try:
            db.session.commit()
            print("Database commit successful")  # Debug print after successful commit
        except Exception as e:
            # If an error occurs, roll back the transaction
            db.session.rollback()
            print(f"Exception occurred: {e}")  # Debug print for exception
            # Then re-raise the exception to be handled by the caller
            raise e
    else:
        print("User not found")  # Debug print if user is not found
        raise ValueError("User not found")

