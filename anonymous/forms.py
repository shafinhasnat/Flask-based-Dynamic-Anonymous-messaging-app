from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed

class SignupForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired(), Length(min=3, max=50)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired(), Length(min=3, max=50)])
	confirm_password = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Signup')

class LoginForm(FlaskForm):
	email = StringField('Email')
	password = PasswordField('Password')
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

class LandingForm(FlaskForm):
	txt_msg = TextAreaField('Your message', validators = [Length(max=180)])
	img_msg = FileField('Upload image', validators = [FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Send Anonymously!')