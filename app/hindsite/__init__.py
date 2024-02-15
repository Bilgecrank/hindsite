"""
Inits variables for the application
"""

from flask import Flask
from flask_bootstrap import Bootstrap5
from hindsite.extensions import db, login_manager, Base


def create_app():
    """
    Application factory to create app.
    """

    app = Flask(__name__)
    app.config.from_object("config.Config")

    bootstrap = Bootstrap5(app)

    login_manager.init_app(app)
    db.Model = Base
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

    return app
