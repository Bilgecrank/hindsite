"""
Inits variables for the application
"""
import os
from dotenv import load_dotenv
from flask import Flask
from hindsite.extensions import bootstrap, db, login_manager, Base


def create_app():
    load_dotenv()
    database_uri = ("mysql+pymysql://"
                    + os.environ['MYSQLUSER'] + ":"
                    + os.environ['MYSQL_ROOT_PASSWORD'] + "@"
                    + os.environ['MYSQLHOST'] + ":"
                    + os.environ['MYSQLPORT'] + "/"
                    + os.environ['MYSQL_DATABASE'])

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']  # Session secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

    login_manager.init_app(app)
    db.Model = Base
    db.init_app(app)

    # TEST OPTION: WIPE DATA FROM DB.
    with app.app_context():
        db.drop_all()
        db.create_all()

    # pylint: disable=wrong-import-position
    from hindsite.routes import routes
    # pylint: enable=wrong-import-position
    app.register_blueprint(routes)
    return app
