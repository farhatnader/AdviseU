from flask import Flask, flash, redirect, render_template, request, session, abort
import os

from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from db_def import *
 

engine = create_engine('sqlite:///users.db', echo=True)
 
Session = sessionmaker(bind=engine)
db_session = Session()


app = Flask(__name__)


@app.route('/')
def home():
	if not session.get('logged_in'):
		# return render_template('login.html')
		return redirect('/login')
	else:
		return render_template('index.html', user=session.get('current_user'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	elif request.method == 'POST':
		username = request.form['username']
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		password = request.form['password']

		if username and firstname and lastname and password:
			query = db_session.query(User).filter(User.username == username)
			for user in query:
				flash('An account already exists with that username!')
				return redirect('/register')

			new_user = User(username, firstname, lastname, password)
			db_session.add(new_user)
			db_session.commit()
			return redirect('/')
		else:
			flash('Missing information!')
			return redirect('/register')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		query = db_session.query(User.id).filter(and_(User.username == username, User.password == password))
		if query.scalar() is not None:
			print('USERR --------------------------------')
			print(username)
			session['logged_in'] = True
			session['current_user'] = username
		else:
			flash('Wrong username/password!')
		return redirect('/')


@app.route('/logout', methods=['POST'])
def logout():
	session['logged_in'] = False
	session['current_user'] = None
	return redirect('/')


if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug = True, host = '0.0.0.0', port = 8080)