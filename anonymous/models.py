from anonymous import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), unique = True, nullable = False)
	email = db.Column(db.String(50), unique = True, nullable = False)
	password = db.Column(db.String(120), nullable = False)
	unique_id = db.Column(db.String(),  unique = True, nullable = False)
	messages = db.relationship('Message', backref = 'author', lazy = True)

	def __repr__(self):
		return f"User('{self.id}', '{self.username}', '{self.email}', '{self.password}')"


class Message(db.Model):
	__tablename__ = 'message'
	id = db.Column(db.Integer, primary_key = True)
	msg = db.Column(db.String(), nullable = True)
	image = db.Column(db.String(), nullable = True)
	date_posted = db.Column(db.DateTime(), nullable = False, default = datetime.utcnow)
	unique_id = db.Column(db.String(), db.ForeignKey('user.unique_id'), nullable = False)
	def __repr__(self):
		return f"Message('{self.title}', '{self.date_posted}')"


class Process(UserMixin):
  def __init__(self,id):
    self.id = id