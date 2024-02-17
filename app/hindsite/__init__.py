"""
Inits variables for the application
"""

from flask import Flask
from app.hindsite.extensions import bootstrap, login_manager
from app.hindsite.tables.base import db


def create_app():
    """
    Application factory to create app.
    """

    app = Flask(__name__)
    app.config.from_object("config.Config")

    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    # TEST OPTION: WIPE DATA FROM DB.
    with app.app_context():
        db.drop_all()
        db.create_all()

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.hindsite.auth.auth import auth
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(auth)

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.hindsite.core.core import core
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(core)

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.hindsite.home.home import home
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(home)

    return app
