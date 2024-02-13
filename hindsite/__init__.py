"""
Inits variables for the application
"""
import os
from dotenv import load_dotenv
from flask import Flask
from hindsite.db_setup import Base
from hindsite.extensions import db, login_manager

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

from hindsite.routes import routes
app.register_blueprint(routes)


