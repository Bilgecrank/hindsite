"""
Template route testing for development
"""
import os
from flask import Blueprint, render_template
from flask_login import login_required

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
