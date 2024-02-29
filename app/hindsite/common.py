"""
Template route testing for base page.
"""

import os
from flask import Blueprint, render_template, make_response
from flask_login import login_required

static_dir = os.path.abspath('static')
common = Blueprint('common',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)


@common.route('/bubble')
@login_required
def bubble():
    """
    Updates the notification badge on the menu button.
    :return:
    """
    count = 1
    return render_template("partials/bubble.html", count=count)
