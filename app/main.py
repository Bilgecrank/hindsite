"""
Activation point for the application.
"""
import datetime
import os

from flask import render_template
from app.db_setup import db, app
from tables import User


@app.route('/')
def index():
    """
    Loads index.html, sets the title and users
    """
    title = 'Deployment Test'
    return render_template('index.html', title=title, users=User.query.all())


with app.app_context():
    db.drop_all()
    db.create_all()
    ollanius = User(first_name='Ollanius',
                    last_name='Pius',
                    display_name='EmperorsGoodBoi',
                    email='astramiliwhat@imperium.net',
                    last_login=datetime.datetime.now())
    fabius = User(first_name='Fabius',
                  last_name='Bile',
                  display_name='FabulousB',
                  email='fabulousbile@chaos.org',
                  last_login=datetime.datetime.now())
    db.session.add(ollanius)
    db.session.add(fabius)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default="80"))
