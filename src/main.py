'''
Template route testing for development
'''
import os

from flask import Flask, render_template

# Needed to redirect default paths to maintain the proposed folder structure
# since Flask looks for static and templates in the root folder of the app
template_dir = os.path.abspath('app/templates')
static_dir = os.path.abspath('app/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route('/')
def index():
    '''
        Loads index.html, sets the title
    '''
    title = 'Deployment Test'
    return render_template('index.html', title=title)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default="80"))
