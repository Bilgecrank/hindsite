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
    # from app.hindsite.history.history import history
    # pylint: enable=wrong-import-position,import-outside-toplevel
    # app.register_blueprint(history)

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.hindsite.home.home import home
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(home)

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.hindsite.group.group import grp
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(grp)

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.hindsite.settings.settings import settings
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(settings)

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.hindsite.retrospective.retrospective import retrospective
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(retrospective)

    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.hindsite.common import common
    # pylint: enable=wrong-import-position,import-outside-toplevel
    app.register_blueprint(common)

    return app
