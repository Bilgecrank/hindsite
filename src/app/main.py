from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

import os

load_dotenv()

database_uri = ("mysql+pymysql://"
                + os.environ['MYSQLUSER'] + ":"
                + os.environ['MYSQL_ROOT_PASSWORD'] + "@"
                + os.environ['MYSQLHOST'] + ":"
                + os.environ['MYSQLPORT'] + "/" 
                + os.environ['MYSQL_DATABASE'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

db = SQLAlchemy(app)
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))

def __init__(self, name):
    self.name = name

@app.route('/')
def index():
    title = 'Deployment Test'
    return render_template('index.html', title=title, users = Users.query.all())

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=os.getenv("PORT", default=80))