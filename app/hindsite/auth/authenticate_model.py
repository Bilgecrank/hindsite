"""
Defines logic flow for the authentication process, additionally manages flask-login
session management.
"""
import re  # For serverside validation of secrets.

import bcrypt
from flask import flash, make_response, redirect, render_template, session, url_for
import flask_login
from app.hindsite.extensions import login_manager, db
from app.hindsite.tables import User, Password
from app.hindsite.common_model import get_user

login_manager.login_view = 'auth.sign_in'


class UserSession(flask_login.UserMixin):
    """
    User session object that store session variables.
    """
    def __init__(self, user_id):
        self.id = user_id

class RegistrationError(Exception):
    """
    Definition for errors raised by the register_user function
    """

    message = None

    def __init__(self, message):
        self.message = message


class LoginError(Exception):
    """
    Definition for errors raised by the login function
    """

    message = None

    def __init__(self, message):
        self.message = message


class QueryError(Exception):
    """
    Defines an issue that arises with a query.
    """
    message = None

    def __init__(self, message):
        self.message = message


@login_manager.user_loader
def user_loader(email: str):
    """
    User loader for login_manager

    :param email: **str** Email user is logging in with.
    :return: **UserSession**
    """
    if not is_user(email):
        return None
    return UserSession(email)


@login_manager.request_loader
def request_loader(request):
    """
    Enables login_manager to load user info from requests.

    :param request: **request** Object containing user info.
    :return: **UserSession**
    """
    email = request.form.get('email')
    if not is_user(email):
        return None
    return UserSession(email)

@login_manager.unauthorized_handler
def unauthorized():
    response = make_response(render_template('401.html'), 401)
    response.headers['hx-redirect'] = url_for('auth.sign_in')
    flash("You must log-in to continue", "error")
    return response


def register_user(email: str, email_compare: str, password: str, password_compare: str):
    """
    Takes in a user's email and password, checks if the email is already associated with an account,
    then checks if the password is a valid entry.

    :param email:
    :param password:
    :return: **User** Returns the user created in registration.

    :raises RegistrationError: Raises this in case of an already extant account or if the password
    is not a valid secret.
    """
    if email != email_compare:
        raise RegistrationError('ERROR: Email and confirm email do not match.')
    if password != password_compare:
        raise RegistrationError('ERROR: Password and confirm password do not match.')
    if is_user(email):
        raise RegistrationError('An account already exists with this email.')
    if not valid_email(email):
        raise RegistrationError('Please enter a valid email.')
    if not valid_secret(password):
        raise RegistrationError(
            'Passwords must at least 12 characters long, include 1 uppercase letter, 1 lowercase '
            'letter, 1 number, and 1 special character (!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~).')
    hashword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User('',
                    email=email,
                    password=Password(password=hashword))
    db.session.add(new_user)
    db.session.commit()
    return new_user


def valid_email(email: str):
    """
    Validates entered emails that largely comply with RFC 5322:
    https://datatracker.ietf.org/doc/html/rfc5322#section-3.4

    :param email: **str** Email to be analyzed.

    :returns: **bool** Whether the email meats the requirements or not.
    """
    return re.fullmatch(
        r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)"
        r"*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",
                        email)


def valid_secret(secret: str):
    """
    Checks if a supplied secret(e.g: password) meets minimum security requirements.

    :param secret: The supplied secret
    :return: **bool** Whether the secret meets the requirements.
    """
    return re.fullmatch(r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!\"#$%&'()*+,-./:;<=>?@\[\]^"
                        r"_`{|}~]).{12,}", secret)


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



def login(email: str, password: str):
    """
    Logs a user into the system, initializing a session.

    :param email: **str** The email of the login request.
    :param password: **str** An unhashed password that should match the account its attached to.
    :return: **str** Returns a string indicating an error or **None** if login was successful.
    """
    if not is_user(email):
        raise LoginError('This email is not attached to an account.')
    if is_users_password(email, password):
        flask_login.login_user(UserSession(email))
        session['groupname'] = None
        session['groupid'] = None
        session['facilitator'] = False
        return True
    return False


def logout():
    """
    Logs a user out of the system by clearing their cookie with flask_login.
    """
    flask_login.logout_user()


def is_user(email: str):
    """
    Returns if the user is actually a user in the database by checking if their
    email returns a result

    :param email: **str** Email to check against the database.
    :returns: **bool** Whether the user record is present in the database.
    """
    return get_user(email) is not None


def is_users_password(email: str, password):
    """
    Checks if a provided password matches the stored password attached to the email's account.

    :param email: The email of the user.
    :param password: The plain-text password provided.
    :return:
    """
    stored_password = get_user(email).password.password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), stored_password)