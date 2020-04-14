from anonymous import app, db, bcrypt, login_manager
from flask import Flask, request, render_template, redirect, url_for, flash
from anonymous.forms import SignupForm, LoginForm, LandingForm
from anonymous.models import User, Message, Process
import os
import secrets
from flask_login import login_user,LoginManager,current_user,logout_user,login_required


@app.route('/')
def Home():
	if current_user.is_active:
		query_user = User.query.filter_by(id=current_user.id).first()
		username = query_user.username
		return redirect(url_for('Dashboard', username=username))
	else:
		return render_template('layout.html')

@app.route('/about')
def About():
	title = 'About'
	text = 'This is about page'
	return render_template('about.html', title=title, text=text)

@app.route('/signup',methods = ['GET', 'POST'])
def Signup():
	form = SignupForm()
	title = 'Signup'
	text = 'This is signup page'
	unique_hex = secrets.token_hex(4)
	if form.validate_on_submit():
		print('Signup form validated')
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, unique_id=str(form.username.data+unique_hex))
		db.session.add(user)
		db.session.commit()
		return render_template('layout.html')
	else:
		print('Signup form error')
	return render_template('signup.html', title=title, form=form, text=text)


@app.route('/login', methods = ['GET','POST'])
def Login():
	form = LoginForm()
	title = 'Login'
	text = 'This is login page'
	if current_user.is_authenticated:
		return redirect(url_for('Dashboard', username=user.username))
	elif form.validate_on_submit():
		print('Login form validated')
		user =  User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			print('++++++++++++++++++++',next_page)
			return redirect(next_page) if next_page else redirect(url_for('Dashboard', username=user.username))
		else:
			return 'login failed!'
	else:
		print('Login form error')
	return render_template('login.html', title=title, text=text, form=form)


@app.route('/logout')
@login_required
def Logout():
	logout_user()
	return redirect(url_for('Home'))


@app.route('/u/<username>', methods=['GET','POST'])
def Landing(username):
	form = LandingForm()
	text = ' landing page'
	database_query =  User.query.filter_by(username=username).first()
	if database_query is None:
		return 'This page doesnt exist'
	else:
		username = database_query.username
		unique_id = database_query.unique_id
		if form.validate_on_submit():
			print('message submitted!')
			msg = Message(msg = form.txt_msg.data, unique_id = str(unique_id))
			db.session.add(msg)
			db.session.commit()
		else:
			print('message submission failed!')
		return render_template('landing.html', username=str(username), form=form)

@app.route('/u/<username>/dashboard')
@login_required
def Dashboard(username):
	print(current_user.is_active,'************************')
	if current_user.is_authenticated:
		query_user = User.query.filter_by(username=username).first()
		user = query_user.unique_id
		user_id = query_user.id
		print(current_user.id, query_user.id)
		if str(query_user.id) == str(current_user.id):
			message = Message.query.filter_by(unique_id=user)
			title = "Dashboard"
			text = "This is dashboard of {}".format(username)
			return render_template('dashboard.html', title=title, text=text, username=username, message=message)
		else:
			return('You are not authenticated')
	else:
		return('You are not authenticated')
