"""
Template route testing for development
"""
import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from app.hindsite.group.group_model import send_invitation, get_invitations, get_invitation, \
    accept_invitation

from app.hindsite.group.group_model import UserSearchError, get_uninvited_users, get_invited_users

static_dir = os.path.abspath('static')
grp = Blueprint('grp',
                  __name__,
                  template_folder='templates',  # relative route to templates dir
                  static_folder=static_dir)


@grp.route('/group', methods=['GET', 'POST'])
@login_required
def group_page():
    """
        Loads group.html, sets the title
    """
    group = session.get('groupid')
    users = []
    if group is not None:
        users = get_invited_users(group)
    return render_template('group.html', title='Group', users=users)


@grp.route('/search-users', methods=['GET', 'POST'])
@login_required
def search_users():
    """
        Loads the user search results
    """
    error = None
    if request.method == 'POST':
        try:
            if 'groupid' not in session \
                    or session['groupid'] is None \
                    or session['groupid'] == 'Select a Group':
                # Tell the user to select a group first.
                return render_template('partials/no-group.html')
            # Load in the uninvited users
            search = request.form['search']
            users = get_uninvited_users(session['groupid'], search)
        except UserSearchError as e:
            error = e.message
        if error is not None:
            flash(error)
            return redirect(url_for('group_page'))
    if request.form['search'] == "":
        users = ""
    return render_template('partials/search-results.html', users=users, term=search)


@grp.route('/send-invite', methods=['GET', 'POST'])
@login_required
def send_invite():
    """
        POST route to send invite codes to other users.
    """
    if request.method == 'POST':
        try:
            term = request.args['search']
            if 'groupid' not in session \
                    or session['groupid'] is None \
                    or session['groupid'] == 'Select a Group':
                # Tell the user to select a group first.
                return render_template('partials/no-group.html')
            # Load in the user arg
            user = request.args['user']
            send_invitation(session['groupid'], user)
            # load in the search results
            # users = get_uninvited_users(session['groupid'], term)
            # users = get_uninvited_users(session['groupid'],request.form['search'])
            return render_template('partials/invite-sent.html', term=term)
        except UserSearchError as ex:
            flash(ex.message)
    return render_template('partials/search-results.html')


@grp.route('/invites', methods=['POST', 'GET'])
@login_required
def invites():
    """
        Loads all the invite codes to be accepted or rejected
    TODO: Put the invite codes into a modal, add decline button, create
    notification bell to open the modal.
    """
    if request.method == 'GET':
        invitations = get_invitations(current_user.id)
        return render_template('partials/invites.html', invitations=invitations)
    if request.method == 'POST':
        group = request.args['group']
        membership = get_invitation(group, current_user.id)
        accept_invitation(membership)
    return render_template('partials/accepted.html')
