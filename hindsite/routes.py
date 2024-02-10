"""
Template route testing for development
"""
from functools import wraps
import os
from dotenv import load_dotenv

from flask_bootstrap import Bootstrap5
from flask import Blueprint, Flask, flash, redirect, render_template, session, url_for

load_dotenv()
# Needed to redirect default paths to maintain the proposed folder structure
# since Flask looks for static and templates in the root folder of the app
template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')
routes = Blueprint('routes',__name__, template_folder=template_dir, static_folder=static_dir)
routes.secret_key = os.environ["SECRET_KEY"]

# Allows us to redirect and display a flash message if login isn't available
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash("you need to login first")
                return redirect(url_for('routes.sign_in'))
    return wrap

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

@routes.route('/sign-in')
def sign_in():
    """
        Loads sign-in.html, sets the title
    """
    title = 'Sign In'
    return render_template('sign-in.html', title=title)

@routes.route('/sign-up')
def sign_up():
    """
        Loads sign-up.html, sets the title
    """
    title = 'Sign up!'
    return render_template('sign-up.html', title=title)

if __name__ == '__main__':
    routes.run(debug=True, port=os.getenv("PORT", default="80"))
