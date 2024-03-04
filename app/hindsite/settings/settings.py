"""
Template route testing for development.

This module is part of the settings feature directory. Users can view and update their account
settings.It includes routes for displaying the settings page, updating user settings such as display
name, email, and password, and deleting the account.
"""
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.hindsite.auth.authenticate_model import is_users_password, logout
from app.hindsite.common_model import get_user
from app.hindsite.settings.settings_model import (update_user_settings,
                                                  get_user_settings,
                                                  UpdateError)

# Blueprint configuration
static_dir = os.path.abspath('static')
settings = Blueprint('settings', __name__,
                     template_folder='templates',  # relative route to templates dir
                     static_folder=static_dir)


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def settings_page():
    """
    Route to display the settings page.

    Returns:
        Rendered template for the settings page with current user settings.
    """
    if request.method == 'POST':
        try:
            user = get_user(current_user.id)
            new_display_name, new_email, new_password = None, None, None

            if not (request.form['display_name'] == 'Enter new display name'
                    or request.form['display_name'] == user.display_name):
                new_display_name = request.form['display_name']

            if not (request.form['email'] == 'Enter new email'
                    or request.form['email'] == user.email):
                new_email = request.form['email']

            if not (request.form['password'] == 'Enter new email'
                    or is_users_password(user.email, request.form['password'])):
                new_password = request.form['password']

            update_user_settings(user,
                                 new_display_name=new_display_name,
                                 new_email=new_email,
                                 new_password=new_password)
            if new_email is not None:
                logout()
                return redirect(url_for('auth.sign_in', error='Sign in using your new email.'))
        except UpdateError as e:
            flash(str(e), 'error')
    return render_template('settings.html',
                           title='Settings',
                           user_settings=get_user_settings(current_user.id))

# # Delete account
# @settings.route('/delete_account', methods=['GET', 'POST'])
# @login_required
# def delete_account():
#     """
#         Route to delete the user's account.

#         Returns:
#             Redirect to the sign-in page with a flash message indicating account
#             deletion or cancellation.
#         """
#     if request.method == 'POST':
#         flash('Account deleted: returned to sign-in page', 'success')
#         return redirect(url_for('auth.sign_in'))
#     flash('Account deletion cancelled', 'canceled')

#     return redirect(url_for('settings.settings_page'))
