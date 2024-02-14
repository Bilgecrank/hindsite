"""
Inits variables for the application
"""

from flask import Flask
from hindsite.extensions import db, login_manager, Base
from hindsite.config import Config


def create_app(config_class=Config):
    """
    Application factory to create app.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    db.Model = Base
    db.init_app(app)

    # TEST OPTION: WIPE DATA FROM DB.
    with app.app_context():
        db.drop_all()
        db.create_all()

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from hindsite.routes import routes
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(routes)
    return app
