"""
Template route testing for development
"""
import os
from flask import Blueprint, render_template, request, session
from flask_login import current_user, login_required

from app.hindsite.common_model import *

static_dir = os.path.abspath('static')
retrospective = Blueprint('retrospective',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)

@retrospective.route('/retrospective')
@login_required
def retrospective_view():
    """
        Loads retrospective.html, sets the title
    """
    title = 'Retrospective'
    board = None
    boards = []
    if 'groupid' in session and session['groupid'] is not None:
        if get_group(int(session.get('groupid'))) is not None:
            boards = get_boards(int(session.get('groupid')))
            board = boards[0]
    return render_template('retrospective.html', title=title, board=board)

@retrospective.route('/retro-test')
@login_required
def retro_test():
    """
    """
    board = None
    boards = []
    if 'groupid' in session and session['groupid'] is not None:
        if get_group(int(session.get('groupid'))) is not None:
            boards = get_boards(int(session.get('groupid')))
            board = boards[0]
    return render_template('partials/retro-test.html', board=board)

# MODALS

@retrospective.route('/rcard-options-modal')
@login_required
def rcard_options_modal():
    """
    """
    return "Card Options"

@retrospective.route('/rfield-options-modal')
@login_required
def rfield_options_modal():
    """
    """
    return "Field Options"

# EDIT ROUTES

@retrospective.route('/redit-card-modal')
@login_required
def redit_card_modal():
    """
    """
    field_id = int(request.args['field_id'])
    card_id = int(request.args['card_id'])
    board_id = int(request.args['board_id'])
    return render_template('partials/redit-card-modal.html', \
                           field_id=field_id, card_id=card_id, board_id=board_id)


@retrospective.route('/redit-card', methods=['GET', 'POST'])
@login_required
def redit_card():
    """
        Takes the data from the modal and updates the card.
    """
    field_id = int(request.args['field_id'])
    card_id = int(request.args['card_id'])
    board_id = int(request.args['board_id'])
    group_id = session.get('groupid')
    card_text = request.form['card-text']
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    card = get_card(card_id, field)
    update_card_message(card, card_text)
    return render_template('partials/card.html', \
                           board_id=board_id, field_id=field_id, card_id=card_id, card=card)

@retrospective.route('/redit-field', methods=['POST', 'GET'])
@login_required
def redit_field():
    """
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    group_id = session.get('groupid')
    field_text = request.form['fieldname']
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    update_field_name(field, field_text)
    return render_template('partials/fields.html', board=board)

@retrospective.route('/redit-field-modal')
@login_required
def redit_field_modal():
    """
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    return render_template('partials/redit-field-modal.html', field_id=field_id, board_id=board_id)

@retrospective.route('/radd-card-modal')
@login_required
def radd_card_modal():
    """
    """
    card_id = int(request.args['card_id'])
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    return render_template('partials/radd-card-modal.html', card_id=card_id, field_id=field_id, board_id=board_id)

@retrospective.route('/radd-card', methods=['POST', 'GET'])
@login_required
def radd_card():
    """
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    card_text = request.form['card-text']
    group_id = session.get('groupid')
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    card = add_card(field, get_user(current_user.id), card_text)

    return render_template('partials/new-card.html', board=board, field=field, card=card)

@retrospective.route('/radd-field-modal')
@login_required
def radd_field_modal():
    """
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    return render_template('partials/radd-field-modal.html', field_id=field_id, board_id=board_id)

@retrospective.route('/radd-field', methods=['POST', 'GET'])
@login_required
def radd_field():
    """
        Takes data from the add-field-modal and adds the field.
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    group_id = session.get('groupid')
    field_text = request.form['fieldname']
    board = get_board(group_id, board_id)
    add_field(board, field_text)
    return render_template('partials/fields.html', board=board, field_id=field_id, board_id=board_id)
