"""
Template route testing for development
"""
import os
from flask import Blueprint, render_template
from flask_login import login_required

static_dir = os.path.abspath('static')
history = Blueprint('history',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)

@history.route('/history')
@login_required
def history_page():
    """
        Loads history.html, sets the title
    """
    title = 'History'
    return render_template('history.html', title=title)
