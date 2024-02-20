"""
Template route testing for development
"""
import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_required
from app.hindsite.group.group_model import send_invitation

from app.hindsite.group.group_model import UserSearchError, get_users

static_dir = os.path.abspath('static')
group = Blueprint('group',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)

@group.route('/group', methods=['GET', 'POST'])
@login_required
def group_page():
    """
        Loads group.html, sets the title
    """
    return render_template('group.html', title='Group')

@group.route('/search-users', methods=['GET', 'POST'])
@login_required
def search_users():
    """
        Loads the user search results
    """

    error = None
    if request.method == 'POST':
        try:
            # get users
            users = get_users(request.form['search'])
        except UserSearchError as e:
            error = e.message
        if error is not None:
            flash(error)
            return redirect(url_for('group_page'))
    if request.form['search'] == "":
        users = ""
    return render_template('partials/search-results.html', users=users)

@group.route('/send-invite', methods=['GET', 'POST'])
@login_required
def send_invite():
    """
        POST route to send invite codes to other users.
    """
    if request.method == 'POST':
        try:
            user = request.args['user']
            send_invitation(session['groupid'], user)
        except UserSearchError as ex:
            flash(ex.message)
        return "Invitation Sent!"
    return render_template('partials/search-results.html')
