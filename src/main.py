'''
Template route testing for development
'''
import os

from flask_bootstrap import Bootstrap5
from flask import Flask, render_template

# Needed to redirect default paths to maintain the proposed folder structure
# since Flask looks for static and templates in the root folder of the app
template_dir = os.path.abspath('app/templates')
static_dir = os.path.abspath('app/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    '''
        Loads index.html, sets the title
    '''
    title = 'Index'
    return render_template('index.html', title=title)

@app.route('/retrospective')
def retrospective():
    '''
        Loads retrospective.html, sets the title
    '''
    title = 'Retrospective'
    return render_template('retrospective.html', title=title)

@app.route('/history')
def history():
    '''
        Loads history.html, sets the title
    '''
    title = 'History'
    return render_template('history.html', title=title)

@app.route('/group')
def group():
    '''
        Loads group.html, sets the title
    '''
    title = 'Group'
    return render_template('group.html', title=title)

@app.route('/settings')
def settings():
    '''
        Loads settings.html, sets the title
    '''
    title = 'Settings'
    return render_template('settings.html', title=title)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default="80"))
