"""
Template route testing for development
"""
import os
from flask import Blueprint, redirect, render_template, request, session, flash
from flask_login import current_user, login_required

from app.hindsite.common_model import get_group, get_boards, get_board, get_field, get_card, \
    update_card_message, update_field_name, add_card, get_user, add_field

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
    if 'groupid' not in session or session.get('groupid') is None:
        flash('Please select a group to enable Retrospective View')
        return redirect('/home')
    print(session.get('groupid'))
    title = 'Retrospective'
    board = None
    boards = []
    if 'groupid' in session and session['groupid'] is not None:
        if get_group(int(session.get('groupid'))) is not None:
            boards = get_boards(int(session.get('groupid')))
            board = boards[0]
    return render_template('retrospective.html', title=title, board=board)

@retrospective.route('/retro-reload')
@login_required
def retro_test():
    """
        Used to load the carousel
    """
    board = None
    boards = []
    if 'groupid' in session and session['groupid'] is not None:
        if get_group(int(session.get('groupid'))) is not None:
            boards = get_boards(int(session.get('groupid')))
            board = boards[0]
    return render_template('partials/retro-reload.html', board=board)

# MODALS

@retrospective.route('/rcard-options-modal')
@login_required
def rcard_options_modal():
    """
        Loads the card options modal, which does nothing right now.
    """
    return render_template('partials/card-options-modal.html')

@retrospective.route('/rfield-options-modal')
@login_required
def rfield_options_modal():
    """
        Loads the field options modal
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    return render_template('partials/rfield-options-modal.html', \
                           field_id=field_id, board_id=board_id)

# GET ROUTES

@retrospective.route('/card')
@login_required
def card_route():
    """
        Card GET route for HTMX reloading
    """
    field_id = int(request.args['field_id'])
    card_id = int(request.args['card_id'])
    board_id = int(request.args['board_id'])
    group_id = session.get('groupid')
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    card = get_card(card_id, field)
    return render_template('partials/card.html', \
                           card=card, board=board, field=field)

@retrospective.route('/field')
@login_required
def field_route():
    """
        Field GET route for HTMX reloading
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    group_id = session.get('groupid')
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    return render_template('partials/field.html', \
                           board=board, field=field)

# EDIT ROUTES

@retrospective.route('/redit-card-modal')
@login_required
def redit_card_modal():
    """
        Loads the edit card modal
    """
    field_id = int(request.args['field_id'])
    card_id = int(request.args['card_id'])
    board_id = int(request.args['board_id'])
    group_id = session.get('groupid')
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    card = get_card(card_id, field)
    return render_template('partials/redit-card-modal.html', \
                           board=board,field=field,card=card)


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
                           board=board, field=field, card=card)

@retrospective.route('/redit-field', methods=['POST', 'GET'])
@login_required
def redit_field():
    """
        POST route for editing fields
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    group_id = session.get('groupid')
    field_text = request.form['fieldname']
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    update_field_name(field, field_text)
    return render_template('partials/field.html', board=board, field=field)

@retrospective.route('/redit-field-modal')
@login_required
def redit_field_modal():
    """
        Loads the edit field modal
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    group_id = session.get('groupid')
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    return render_template('partials/redit-field-modal.html', \
                           field=field,board=board)

# ADD ROUTES

@retrospective.route('/radd-card-modal')
@login_required
def radd_card_modal():
    """
        Loads the add card modal
    """
    card_id = int(request.args['card_id'])
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    return render_template('partials/radd-card-modal.html', \
                           card_id=card_id, field_id=field_id, board_id=board_id)

@retrospective.route('/radd-card', methods=['POST', 'GET'])
@login_required
def radd_card():
    """
        Post route for adding cards
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    card_text = request.form['card-text']
    group_id = session.get('groupid')
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    card = add_card(field, get_user(current_user.id), card_text)

    return render_template('partials/card.html', board=board, field=field, card=card)

@retrospective.route('/radd-field-modal')
@login_required
def radd_field_modal():
    """
        Loads the add field modal
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
    board = get_board(group_id, board_id)
    field = get_field(field_id, board)
    group_id = session.get('groupid')
    field_text = request.form['fieldname']
    add_field(board, field_text)
    return render_template('partials/retro-reload.html', board=board, field=field)
