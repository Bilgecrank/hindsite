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


@common.route('/retro_active')
@login_required
def retro_active():
    """
    Returns whether a retrospective is active for the current group.
    :return:
    """
    count = 1
    return render_template("partials/retro_active.html", count=count)


@common.route('/invite_count')
@login_required
def invite_count():
    """
    Returns a number current invites.
    :return:
    """
    count = 1
    return render_template("partials/invite_count.html", count=count)


def get_retro_active(group_id: int):
    """

    :return: **int**
    """
    return retro_count


def get_num_of_invites():

    return invite_count
