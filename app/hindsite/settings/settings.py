"""
Template route testing for development
"""
import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user

from app.hindsite import db
from app.hindsite.settings.settings_model import update_user_display_name, update_user_settings
from app.hindsite.tables import User

static_dir = os.path.abspath('static')
settings = Blueprint('settings',
                     __name__,
                     template_folder='templates',  # relative route to templates dir
                     static_folder=static_dir)


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def settings_page():
    """
        Loads settings.html, sets the title
    """
    return render_template('settings.html', title='Settings', user_settings='user_settings')


@settings.route('/update_settings', methods=['GET', 'POST'])
@login_required
def update_settings():
    # Fetch the current user instance from the database
    user = User.query.get(current_user.id) # session var

    if user:
        # Update user fields with new values from the form
        user.display_name = request.form.get('display_name', user.display_name)
        user.email = request.form.get('email', user.email)

        if 'password' in request.form and request.form['password']:
            user.set_password(request.form['password'])

        try:
            # Commit the changes to the database
            db.session.commit()
            flash('Settings updated successfully!', 'success')
        except Exception as e:
            # Roll back in case of error
            db.session.rollback()
            flash('An error occurred while updating settings.', 'error')
            # Log the error for debugging
            app.logger.error(f'Error updating settings for user {user.id}: {e}')
    else:
        flash('User not found.', 'error')

    return redirect(url_for('settings.settings_page'))


# Update display name
@settings.route('/update_display_name', methods=['GET', 'POST'])
@login_required
def update_display_name():
    print(f"user_id check before update_display_name:{current_user.id}")  # Debug print

    if request.method == 'POST':
        # Extract the new display name from the form data
        new_display_name = request.form.get('display_name')
        print(f"New display name from form: {new_display_name}")  # Debug print

        # Validate the new display name
        if not new_display_name:
            flash('Display name cannot be empty.', 'error')
            return redirect(url_for('settings.settings_page'))

        try:
            print(f"Updating display name for user ID {current_user.id}")  # Debug print
            # Update the user's display name in the database
            update_user_display_name(current_user.id, new_display_name)

            print(f"Display name updated successfully to {new_display_name}")  # Debug print
            # Provide a success message
            flash('Display name updated successfully!', 'success')
        except Exception as e:
            # In case of an error, roll back and show an error message
            print(f"Error updating display name: {e}")  # Debug print
            flash(f'An error occurred: {str(e)}', 'error')

        # Redirect to the settings page or another relevant page
        return redirect(url_for('settings.settings_page'))

    return redirect(url_for('settings.settings_page'))


'''
# Update email address
@settings.route('/update_email', methods=['GET', 'POST'])
@login_required
def update_email():
    # Logic to update the user's email address
    ...


# Update password
@settings.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    # Logic to update the user's password
    ...


# Delete account
@settings.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    # Logic to delete the user's account
    ...
    '''
