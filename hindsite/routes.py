"""
Template route testing for development
"""
from functools import wraps
import os
from flask import Blueprint, flash, redirect, render_template, session, url_for, request
from flask_login import login_required

import hindsite.authenticate as auth

template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')
routes = Blueprint('routes',
                   __name__,
                   template_folder=template_dir,
                   static_folder=static_dir)
"""
def login_required(f):
    """"""
        Allows us to redirect and display a flash message if login isn't available
    """"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        flash("you need to login first")
        return redirect(url_for('routes.sign_in'))
    return wrap
"""


@routes.route('/')
@login_required
def index():
    """
        Loads index.html, sets the title
    """
    title = 'Index'
    return render_template('index.html', title=title)


@routes.route('/retrospective')
@login_required
def retrospective():
    """
        Loads retrospective.html, sets the title
    """
    title = 'Retrospective'
    return render_template('retrospective.html', title=title)


@routes.route('/history')
@login_required
def history():
    """
        Loads history.html, sets the title
    """
    title = 'History'
    return render_template('history.html', title=title)


@routes.route('/group')
@login_required
def group():
    """
        Loads group.html, sets the title
    """
    title = 'Group'
    return render_template('group.html', title=title)


@routes.route('/settings')
@login_required
def settings():
    """
        Loads settings.html, sets the title
    """
    title = 'Settings'
    return render_template('settings.html', title=title)


@routes.route('/sign-in', methods = ['POST', 'GET'])
def sign_in():
    """
        Loads sign-in.html, sets the title
    """
    error = None
    if request.method == 'POST':
        try:
            auth.login(request.form['email'],
                       request.form['password'])
            return redirect(url_for('routes.index'))
        except auth.LoginError as e:
            error = e.message
    title = 'Sign In'
    if error is not None:
        flash(error)
    return render_template('sign-in.html', title=title, error=error)


@routes.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    error = ''
    if request.method == 'POST':  # Triggers if a user hits submit on a registration form.
        try:
            auth.register_user(request.form['email'],
                               request.form['password'])
            return redirect(url_for('routes.sign-in'))
        except auth.RegistrationError as e:
            error = e.message
    title = 'Sign up!'
    return render_template('sign-up.html', title=title, error=error)

