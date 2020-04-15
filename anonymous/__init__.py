from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfasdfasdf8709asd8f7a9s8dfyuiashdfh'

ENV = 'Prod'
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:19971904@localhost/hackathon'
    app.debug = True
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ecnlsyoyoyxfhk:f99fe6674b2933a0b3127357f9c25f7600672b47e5e228fb454ad5f1d1bc312f@ec2-18-235-20-228.compute-1.amazonaws.com:5432/dbcfa2803jjvgq'
	app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from anonymous.models import Process

bcrypt = Bcrypt()

login_manager = LoginManager(app)
login_manager.login_view = "Login"
login_manager.login_message = 'Access denied! Please login first.'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(user_id):
    return Process(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    print('fuk off')
    return redirect(url_for('Login'))

# from anonymous.models import User
# db.create_all()

from anonymous import routes