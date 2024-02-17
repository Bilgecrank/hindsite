"""
Template route testing for development
"""
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.hindsite.home.models import create_group, get_groups, GroupAddError

static_dir = os.path.abspath('static')
home = Blueprint('home',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)

@home.route('/home', methods=['GET', 'POST'])
@login_required
def homepage():
    """
        Loads home.html, sets the title
    """
    groups = get_groups(current_user.id)
    return render_template('home.html', title='Home', groups=groups)

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
