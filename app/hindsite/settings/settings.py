"""
Template route testing for development.

This module is part of the settings feature directory. Users can view and update their account
settings.It includes routes for displaying the settings page, updating user settings such as display
name, email, and password, and deleting the account.
"""
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.hindsite.settings.settings_model import update_user_settings, get_user_settings, UpdateError
from app.hindsite.tables import User

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
    return render_template('settings.html', title='Settings', user_settings=get_user_settings(User.email))


@settings.route('/update_display_name', methods=['POST'])
@login_required
def update_display_name():
    """
        Route to update the user's display name.

        Returns:
            Redirect to the settings page with a flash message indicating success or failure.
        """
    try:
        new_display_name = request.form['display_name']
        update_user_settings(email=User.email, new_display_name=new_display_name)
        flash('Display name successfully updated.')
    except UpdateError as e:
        flash(str(e), 'error')
    return redirect(url_for('settings.settings_page'))


# Update email address
@settings.route('/update_email', methods=['GET', 'POST'])
@login_required
def update_email():
    """
        Route to update the user's email address.

        Returns:
            Redirect to the settings page with a flash message indicating success or failure.
        """
    try:
        new_email = request.form['email']
        update_user_settings(email=User.email, new_email=new_email)
        flash('Email successfully updated: redirected to sign in page.')
    except UpdateError as e:
        flash(str(e), 'error')

    return redirect(url_for('auth.sign_in'))


# Update password
@settings.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    """
        Route to update the user's password.

        Returns:
            Redirect to the settings page with a flash message indicating success or failure.
        """
    try:
        new_password = request.form['password']
        update_user_settings(email=User.email, new_password=new_password)
        flash('Password successfully updated.')
    except UpdateError as e:
        flash(str(e), 'error')

    return redirect(url_for('settings.settings_page'))


# Delete account
@settings.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    """
        Route to delete the user's account.

        Returns:
            Redirect to the sign-in page with a flash message indicating account deletion or cancellation.
        """
    if request.method == 'POST':
        flash('Account deleted: returned to sign-in page', 'success')
        return redirect(url_for('auth.sign_in'))
    else:
        flash('Account deletion cancelled', 'canceled')

    return redirect(url_for('settings.settings_page'))


