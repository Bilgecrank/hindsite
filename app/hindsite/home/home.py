"""
Template route testing for development
"""
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.hindsite.home.home_model import create_group, GroupAddError, get_invitations
from app.hindsite.common_model import get_groups

static_dir = os.path.abspath('static')
home = Blueprint('home',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)

@home.route('/')
def index():
    """
        Just redirects to home at the root of the page.
    """
    return redirect(url_for('home.homepage'))

@home.route('/home', methods=['GET', 'POST'])
@login_required
def homepage():
    """
        Loads home.html, sets the title
    """
    selected = "Select Group"
    groups = get_groups(current_user.id)
    if request.method == 'POST':
        try:
            current_user.group = request.args['groupname']
        except Exception:
            flash('There was an error.')
        if current_user.group != None:
            selected = current_user.group
        return render_template('partials/dropdown.html', title='Home', groups=groups, selected=selected)
    
    return render_template('home.html', title='Home', groups=groups, selected=selected)

@home.route('/invites')
@login_required
def invites():
    """
        Loads all the invite codes to be accepted or rejected
    """
    invites = get_invitations(current_user.id)
    return render_template('partials/invites.html', invites=invites)

@home.route('/add-group', methods=['GET', 'POST'])
@login_required
def group_add():
    """
        The route for the add group dropdown item.
    """
    error = None
    if request.method == 'POST':
        try:
            create_group(request.form['groupname'], current_user.id)
            current_user.group = request.form['groupname']
        except GroupAddError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/modal')
@login_required
def modal():
    """
        Route to retrieve the modal using HTMx
    """
    groups = get_groups(current_user.id)
    return render_template('partials/modal.html', groups=groups)
