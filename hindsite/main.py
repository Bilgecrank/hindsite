"""
Activation point for the application.
"""
import datetime
import os

import bcrypt
from flask_bootstrap import Bootstrap5
from flask import render_template
from hindsite.db_setup import db, app
from hindsite.tables import User, Password
import hindsite.sql_query as query
import hindsite.authenticate as auth

bootstrap = Bootstrap5(app)
@app.route('/')
def index():
    """
    Loads index.html, sets the title and users
    """
    title = 'Back-End Deployment Test'
    return render_template('index.html',
                           title=title,
                           users=User.query.all(),
                           result=[query.get_user('astramiliwhat@imperium.net'),
                                   query.is_user('astramiliwhat@imperium.net'),
                                   query.get_hashword(query.get_user('astramiliwhat@imperium.net').id),
                                   auth.login('astramiliwhat@imperium.net', 'Buh12_buh12_buh12')])


with app.app_context():
    db.drop_all()
    db.create_all()
    auth.register_user('astramiliwhat@imperium.net', 'Buh12_buh12_buh12')
    fabius = User(display_name='FabulousB',
                  email='fabulousbile@chaos.org')
    fabius.password = [Password(user_id=fabius,
                           password='Fabulous')]
    db.session.add(fabius)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default="80"))
