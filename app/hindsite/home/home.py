"""
Template route testing for development
"""
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from app.hindsite.home.home_model import create_group, GroupAddError
from app.hindsite.common_model import *

static_dir = os.path.abspath('static')
home = Blueprint('home',
                   __name__,
                   template_folder='templates',    # relative route to templates dir
                   static_folder=static_dir)

@home.route('/')
def index():
    """
        Just redirects to home at the root of the page.
    """
    return redirect(url_for('home.homepage'))

@home.route('/home', methods=['GET', 'POST'])
@login_required
def homepage():
    """
        Checks the authorization state and returns the correct
        function depending on what the facilitator session variable
        value is.
    """
    if 'groupname' not in session or session['groupname'] is None:
        #Ensures session contains groupname and sets a default value
        session['groupname'] = "Select a Group"
    selected = session['groupname']

    groups = get_groups(current_user.id)

    # Need to check for 'POST' first in case there's a redirect from a participant
    if request.method == 'POST':
        try:
            session['groupname'] = request.args['groupname']
            session['groupid'] = int(request.args['group_id'])
            group_id = session.get('groupid')
            ownership = get_ownership(current_user.id, group_id)
            session['facilitator'] = ownership
        except Exception as ex:
            print(ex)
        if 'groupname' in session:
            selected = session['groupname']

    board = None
    boards = []
    if 'groupid' in session and session['groupid'] is not None:
        if get_group(session.get('groupid')) is not None:
            # a group is selected, so we can populate the boards
            group_id = session.get('groupid')
            boards = get_boards(group_id)
            if boards is None or boards == []:
                #creates the board defaults
                #adds the boards to the board selector
                board = create_board(group_id)
                field = add_field(board, "New Category")
                add_card(field, get_user(current_user.id), 'Enter Card Data')
            boards = get_boards(group_id)
            #populates the board selector
            #selects the most recent board
            board = boards[0]

    return authorized_routes(facilitator_route(selected, groups, board), \
                             participant_route(selected, groups, board))

def participant_route(selected: str, groups: Group, board: Board):
    """
        Loads home.html, sets the title and loads in the group
        selection dropdown. Periodically checks for invites sent
        from other users to their groups and loads them.
    """
    return render_template('home.html', title='Home', groups=groups, selected=selected, board=board)

def facilitator_route(selected: str, groups: Group, board: Board):
    """
        Route for Facilitator mode
    """
    return render_template('facilitator-home.html', title='Facilitator Home', \
                           groups=groups, selected=selected, board=board)


# EDIT ROUTES AND POST ROUTES
@home.route('/edit-card', methods=['POST', 'GET'])
@login_required
def card_edit():
    """
        Route modal POSTs to for changing a card text
    """
    error = None
    if request.method == 'POST':
        try:
            card_text = request.form['card-text']
            field_id = int(request.args['field_id'])
            board_id = int(request.args['board_id'])
            card_id = int(request.args['card_id'])
            group_id = session.get('groupid')
            board = get_board(group_id, board_id)
            field = get_field(field_id, board)
            card = get_card(card_id, field)
            update_card_message(card, card_text)
        except CardError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/edit-card-modal')
@login_required
def card_modal():
    """
        Route to retrieve the field modal using HTMx
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    card_id = int(request.args['card_id'])
    return render_template('partials/edit-card-modal.html', \
                           field_id=field_id, board_id=board_id, card_id=card_id)

@home.route('/edit-field', methods=['GET','POST'])
@login_required
def edit_field():
    """
        Route modal POSTs to for renaming a field
    """
    error = None
    if request.method == 'POST':
        try:
            fieldname = request.form['fieldname']
            field_id = int(request.args['field_id'])
            board_id = int(request.args['board_id'])
            group_id = session.get('groupid')
            board = get_board(group_id, board_id)
            field = get_field(field_id, board)
            update_field_name(field, fieldname)
        except FieldError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/edit-field-modal')
@login_required
def edit_field_modal():
    """
        Route to retrieve the field modal using HTMx
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    return render_template('partials/edit-field-modal.html', \
                           field_id=field_id, board_id=board_id)

# ADD ROUTES AND POST ROUTES

@home.route('/add-group', methods=['GET', 'POST'])
@login_required
def group_add():
    """
        The route for the add group dropdown item.
    """
    error = None
    group = None
    groupname = "Select a Group"
    if request.method == 'POST':
        try:
            groupname = request.form['groupname']
            group = create_group(groupname, current_user.id)
            session['groupname'] = group.name
        except GroupAddError as e:
            error = e.message
    if error is not None:
        flash(error)
    # Redirects to home and selects the groupname and group_id
    if group is not None:
        return redirect(url_for('home.homepage', groupname=group.name, group_id=group.id), code=307)
    return redirect(url_for('home.homepage'))


@home.route('/add-group-modal')
@login_required
def group_add_modal():
    """
        Route to retrieve the modal using HTMx
    """
    groups = get_groups(current_user.id)
    return render_template('partials/add-group-modal.html', groups=groups)

@home.route('/add-field', methods=['GET','POST'])
@login_required
def new_field():
    """
        Route modal POSTs to for adding a field
    """

    error = None
    if request.method == 'POST':
        try:
            fieldname = request.form['fieldname']
            board_id = int(request.args['board_id'])
            group_id = session.get('groupid')
            board = get_board(group_id, board_id)
            add_field(board, fieldname)
        except FieldError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/add-field-modal')
@login_required
def add_field_modal():
    """
        Route to retrieve the add field modal using HTMx
    """
    board_id = int(request.args['board_id'])
    field_id = int(request.args['field_id'])
    return render_template('partials/add-field-modal.html', \
                           board_id=board_id, field_id=field_id)


@home.route('/add-card', methods=['GET','POST'])
@login_required
def new_card():
    """
        Route modal POSTs to for adding a card
    """

    error = None
    if request.method == 'POST':
        try:
            card_text = request.form['card-text']
            field_id = int(request.args['field_id'])
            board_id = int(request.args['board_id'])
            group_id = session.get('groupid')
            board = get_board(group_id, board_id)
            field = get_field(field_id, board)
            add_card(field, get_user(current_user.id), card_text)
        except CardError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/add-card-modal')
@login_required
def add_card_modal():
    """
        Route to retrieve the field modal using HTMx
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    return render_template('partials/add-card-modal.html', \
                           field_id=field_id, board_id=board_id)

# OPTIONS ROUTES AND MODALS
@home.route('/card-options', methods=['GET','POST'])
@login_required
def card_options():
    """
        Route modal POSTs to for card options
    """

    error = None
    if request.method == 'POST':
        try:
            card_text = request.form['card-text']
            field_id = int(request.args['field_id'])
            board_id = int(request.args['board_id'])
            group_id = session.get('groupid')
            board = get_board(group_id, board_id)
            field = get_field(field_id, board)
            add_card(field, get_user(current_user.id), card_text)
        except CardError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/card-options-modal')
@login_required
def card_options_modal():
    """
        Route to retrieve the field modal using HTMx
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    card_id = int(request.args['card_id'])
    return render_template('partials/card-options-modal.html', \
                           field_id=field_id, board_id=board_id, card_id=card_id)

@home.route('/field-options', methods=['GET','POST'])
@login_required
def field_options():
    """
        Route modal POSTs to for card options
    """

    error = None
    if request.method == 'POST':
        try:
            field_id = int(request.args['field_id'])
            board_id = int(request.args['board_id'])
            group_id = session.get('groupid')
            board = get_board(group_id, board_id)
        except CardError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/field-options-modal')
@login_required
def field_options_modal():
    """
        Route to retrieve the field modal using HTMx
    """
    field_id = int(request.args['field_id'])
    board_id = int(request.args['board_id'])
    group_id = session.get('groupid')
    board = get_board(group_id, board_id)
    return render_template('partials/field-options-modal.html', \
                           field_id=field_id, board_id=board_id, board=board)

# DELETE ROUTES
@home.route('/delete-card', methods=['GET','POST'])
@login_required
def delete_card():
    """
        Route to delete the selected card
    """
    if request.method == 'POST':
        card_id = int(request.args['card_id'])
        field_id = int(request.args['field_id'])
        board_id = int(request.args['board_id'])
        group_id = session.get('groupid')
        board = get_board(group_id, board_id)
        field = get_field(field_id, board)
        card = get_card(card_id, field)
        card = toggle_archive_card(card)
    return redirect(url_for('home.homepage'))

@home.route('/delete-field', methods=['GET','POST'])
@login_required
def delete_field():
    """
        Route to delete the selected field
    """
    if request.method == 'POST':
        field_id = int(request.args['field_id'])
        board_id = int(request.args['board_id'])
        group_id = session.get('groupid')
        board = get_board(group_id, board_id)
        field = get_field(field_id, board)
        field = toggle_archive_field(field)
    return redirect(url_for('home.homepage'))

@home.route('/user-display')
@login_required
def display_user():
    """
        Used to show the current logged in user.
    """
    user = current_user.id
    return render_template('partials/user-display.html', user=user)
