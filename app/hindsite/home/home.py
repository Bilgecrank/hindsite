"""
Template route testing for development
"""
import datetime
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from app.hindsite.home.home_model import create_group, GroupAddError
from app.hindsite.common_model import CardError, FieldError, add_card, add_field, \
        create_board, get_boards, get_card, get_field, get_fields, get_groups, authorized, \
        get_board, get_user, set_start_date_for_board, update_card_message, update_field_name

#TODO:  Remove padding for cards in facilitator-home
#TODO:  Set max size for cards and include overflow-hidden in classes
#TODO:  Create routes for edit-card and rename-field
#TODO:  Put field name and buttons into a span
#           Justify self right for controls
#           Each element has own link

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

    #TODO: The first version below is the correct route. Uncomment it to enable 
    # proper routing.
    #
    # The second version below is to test/develop facilitator_route()

    # return authorized(facilitator_route(selected), participant_route(selected))
    return authorized(participant_route(selected), facilitator_route(selected)) #TODO: TESTING

def participant_route(selected: str):
    """
        Loads home.html, sets the title and loads in the group
        selection dropdown. Periodically checks for invites sent
        from other users to their groups and loads them.
    """
    groups = get_groups(current_user.id)
    if request.method == 'POST':
        try:
            session['groupname'] = request.args['groupname']
            session['groupid'] = request.args['group_id']
        except GroupAddError as ex:
            flash(ex.message)
        if 'groupname' in session:
            selected = session['groupname']
        return render_template('partials/dropdown.html', title='Home', \
                               groups=groups, selected=selected)
    
    return render_template('home.html', title='Home', groups=groups, selected=selected)

def facilitator_route(selected: str):
    """
        Route for Facilitator mode
    """
    groups = get_groups(current_user.id)
    board = None
    boards = None
    # TODO: Get the boards for the group
    if 'groupid' in session and session['groupid'] is not None:
        # a group is selected, so we can populate the boards
        group_id = session.get('groupid')
        boards = get_boards(group_id)
        if boards is None or boards == []:
            #creates the board defaults
            #adds the boards to the board selector
            board = create_board(group_id)
            field = add_field(board, "New Category")
            add_card(field, get_user(current_user.id), 'Enter Card Data')
        else:
            #populates the board selector
            #selects the most recent board

            #TODO: add a selection method for the board
            board = boards[0]

    if request.method == 'POST':
        try:
            session['groupname'] = request.args['groupname']
            session['groupid'] = request.args['group_id']
        except GroupAddError as ex:
            flash(ex.message)
        if 'groupname' in session:
            selected = session['groupname']
        return render_template('facilitator-home.html', title='Facilitator Home', \
                               groups=groups, selected=selected, board=board)
    return render_template('facilitator-home.html', title='Facilitator Home', \
                           groups=groups, selected=selected, board=board)

@home.route('/facilitator-display', methods=['GET', 'POST'])
@login_required
def facilitator_display():
    """
        Route to retrieve the cards using HTMx polling
    """
    groupid = ''
    board = None
    if session.get('groupid') is not None:
        groupid = session.get('groupid')
        boards = get_boards(groupid, False)
        board = boards[0]
    return render_template('partials/facilitator-blob.html', title='Home', board=board)


# MODAL ROUTES AND POST ROUTES
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
            board = get_board(session['groupid'], board_id)
            field = get_field(field_id, board)
            card = get_card(card_id, field)
            print("field_id %s board_id %s card_id %s" %(field_id, board_id, card_id))
            update_card_message(card, card_text)
        except CardError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/card-modal')
@login_required
def card_modal():
    """
        Route to retrieve the field modal using HTMx
    """
    field_id = request.args['field_id']
    board_id = request.args['board_id']
    card_id = request.args['card_id']
    return render_template('partials/edit-card-modal.html', \
                           field_id=field_id, board_id=board_id, card_id=card_id)

@home.route('/rename-field', methods=['GET','POST'])
@login_required
def rename_field():
    """
        Route modal POSTs to for renaming a field
    """
    
    error = None
    if request.method == 'POST':
        try:
            fieldname = request.form['fieldname']
            field_id = int(request.args['field_id'])
            board_id = int(request.args['board_id'])
            board = get_board(session['groupid'], board_id)
            field = get_field(field_id, board)
            update_field_name(field, fieldname)
        except FieldError as e:
            error = e.message
    if error is not None:
        flash(error)
    return redirect(url_for('home.homepage'))

@home.route('/field-modal')
@login_required
def field_modal():
    """
        Route to retrieve the field modal using HTMx
    """
    field_id = request.args['field_id']
    board_id = request.args['board_id']
    return render_template('partials/edit-field-modal.html', \
                           field_id=field_id, board_id=board_id)

@home.route('/add-group', methods=['GET', 'POST'])
@login_required
def group_add():
    """
        The route for the add group dropdown item.
    """
    error = None
    if request.method == 'POST':
        try:
            groupname = request.form['groupname']
            group = create_group(groupname, current_user.id)
            session['groupname'] = group.name
            #TODO: Create a default board
        except GroupAddError as e:
            error = e.message
    if error is not None:
        flash(error)
    #Redirects to home and selects the groupname and group_id
    return redirect(url_for('home.homepage', groupname=groupname, group_id=group.id), code=307)

@home.route('/group-modal')
@login_required
def group_modal():
    """
        Route to retrieve the modal using HTMx
    """
    groups = get_groups(current_user.id)
    return render_template('partials/add-group-modal.html', groups=groups)
