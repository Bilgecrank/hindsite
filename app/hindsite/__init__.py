"""
Inits variables for the application
"""

from flask import Flask
from app.hindsite.extensions import bootstrap, login_manager
from app.hindsite.extensions import db


def create_app():
    """
        Application factory to create app. Initializes the configuration which loads the
        environment variables, then initializes bootstrap, the login_manager, and the 
        database. 
    """

    app = Flask(__name__)
    app.config.from_object("config.Config")

    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    # Blueprints are registered and imported as shown below. The registration order doesn't
    # matter, so long as the pylint statements are around the import and the blueprint is
    # registered directly below it.

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

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.hindsite.group.group import group
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(group)

    return app
