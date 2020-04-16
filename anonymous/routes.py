from anonymous import app, db, bcrypt, login_manager
from flask import Flask, request, render_template, redirect, url_for, flash
from anonymous.forms import SignupForm, LoginForm, LandingForm
from anonymous.models import User, Message, Process
import os
import secrets
from flask_login import login_user,LoginManager,current_user,logout_user,login_required
import base64


@app.route('/')
def Home():
	if current_user.is_active:
		query_user = User.query.filter_by(id=current_user.id).first()
		username = query_user.username
		return redirect(url_for('Dashboard', username=username))
	else:
		return render_template('home.html')

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
	try:
		if form.validate_on_submit():
			print('Signup form validated')
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = User(username=form.username.data, email=form.email.data, password=hashed_password, unique_id=str(form.username.data+unique_hex))
			db.session.add(user)
			db.session.commit()
			flash(f'Your account has been created successfully! You are able to log in', 'success')
			return redirect(url_for('Login'))
		else:
			print('////////************Signup form error')
			pass
	except:
		flash(f'This username or email address is already taken!', 'danger')
		return redirect(url_for('Signup'))
	return render_template('signup.html', title=title, form=form, text=text)


@app.route('/login', methods = ['GET','POST'])
def Login():
	form = LoginForm()
	title = 'Login'
	text = 'This is login page'
	if current_user.is_active:
		query_user = User.query.filter_by(id=current_user.id).first()
		username = query_user.username
		return redirect(url_for('Dashboard', username=username))
	if current_user.is_authenticated:
		return redirect(url_for('Dashboard', username=user.username))
	elif form.validate_on_submit():
		print('Login form validated')
		user =  User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			# print('++++++++++++++++++++',next_page)
			flash(f'Welcome to your dashboard!!', 'success')
			return redirect(next_page) if next_page else redirect(url_for('Dashboard', username=user.username))
		else:
			flash(f'Login failed! Check your email and password', 'danger')
			return render_template('login.html', title=title, text=text, form=form)
	else:
		# flash(f'Error occurred!!', 'danger')
		return render_template('login.html', title=title, text=text, form=form)
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
		text = 'Message sent anonymously to {}!!'.format(username)
		unique_id = database_query.unique_id
		if form.validate_on_submit():
			print('message submitted!')
			image = form.img_msg.data
			try:
				b64_image = base64.b64encode(image.read()).decode()
				# print('++++****+++',b64_image)
				msg = Message(msg = form.txt_msg.data, image = b64_image, unique_id = str(unique_id))
			except:
				msg = Message(msg = form.txt_msg.data, unique_id = str(unique_id))
			 	
			# msg = Message(msg = form.txt_msg.data, unique_id = str(unique_id))
			db.session.add(msg)
			db.session.commit()
			if current_user.is_active:
				query_user = User.query.filter_by(id=current_user.id).first()
				username = query_user.username
				return redirect(url_for('Dashboard', username=username))
			else:
				text = "Message sent anonymously to {}!!".format(username)
				flash(f'{text}', 'success')
				return render_template('home.html', text=text)
		else:
			print('message submission failed!')
		return render_template('landing.html', username=str(username), form=form)

@app.route('/u/<username>/dashboard')
@login_required
def Dashboard(username):
	# print(current_user.is_active,'************************')
	if current_user.is_authenticated:
		query_user = User.query.filter_by(username=username).first()
		user = query_user.unique_id
		user_id = query_user.id
		print(current_user.id, query_user.id)
		if str(query_user.id) == str(current_user.id):
			message = Message.query.filter_by(unique_id=user)
			title = "Dashboard"
			text = "Dashboard of {}".format(username)
			url = username.replace(" ", "%20") 
			return render_template('dashboard.html', title=title, text=text, username=username, message=message, url=url)
		else:
			return redirect(url_for('Home'))
	else:
		return redirect(url_for('Home'))
