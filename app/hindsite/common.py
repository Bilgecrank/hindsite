"""
Template route testing for base page.
"""

import os
from datetime import datetime

from flask import Blueprint, render_template, make_response, session
from flask_login import login_required, current_user

from app.hindsite.common_model import get_boards
from app.hindsite.group.group_model import get_invitations

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

    count = get_num_of_invites()
    # Only return one for active retrospective.
    if get_retro_active() > 0:
        count += 1
    return render_template("partials/bubble.html", count=count)


@common.route('/retro_active')
@login_required
def retro_active():
    """
    Returns whether a retrospective is active for the current group.
    :return:
    """
    count = get_retro_active()
    return render_template("partials/retro_active.html", count=count)


@common.route('/invite_count')
@login_required
def invite_count():
    """
    Returns a number current invites.
    :return:
    """
    count = get_num_of_invites()
    return render_template("partials/invite_count.html", count=count)


def get_retro_active():
    """
    Checks for any active retrospectives.

    :return: **int**
    """
    retro_count = 0
    if 'groupid' not in session \
            or session['groupid'] is None \
            or session['groupid'] == 'Select a Group':
        # User has not selected a group..
        return 0
    boards = get_boards(session['groupid'])
    for board in boards:
        if datetime.now() > board.start_time:
            if board.end_time is not None:
                if datetime.now() < board.end_time:
                    retro_count += 1
            else:
                retro_count += 1
    return retro_count


def get_num_of_invites():
    """
    Returns the number of active invites attached to the cou

    :return:
    """
    return len(get_invitations(current_user.id))
