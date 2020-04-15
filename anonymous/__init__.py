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
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iprxgsxaxsuvkl:aee482552a5736d7defda951e4edf5615015c8c1855b928ae642ddd2cd58d311@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d5nnbjsi33d9k2'
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