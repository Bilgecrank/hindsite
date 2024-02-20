"""
Template route testing for development
"""
import os
from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required
from app.hindsite.auth.authenticate_model import LoginError, \
login, register_user, logout, RegistrationError

static_dir = os.path.abspath('static')
auth = Blueprint('auth',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)


@auth.route('/sign-in', methods = ['POST', 'GET'])
def sign_in():
    """
        Loads sign-in.html, sets the title
    """
    error = None
    if request.method == 'POST':
        try:
            login(request.form['email'],
                  request.form['password'])
            return redirect(url_for('home.homepage'))
        except LoginError as e:
            error = e.message
    title = 'Sign In'
    if error is not None:
        flash(error)
    return render_template('sign-in.html', title=title)


@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    """
        Allows user registration. 
    """
    error = ''
    if request.method == 'POST':  # Triggers if a user hits submit on a registration form.
        try:
            register_user(request.form['email'],
                               request.form['password'])
            return redirect(url_for('home.homepage'))
        except RegistrationError as e:
            error = e.message
            flash(error)
    title = 'Sign up!'
    return render_template('sign-up.html', title=title)

@auth.route('/sign-out')
@login_required
def sign_out():
    """
        Allows the user to sign-out
    """
    logout()
    return redirect(url_for('auth.sign_in'))
