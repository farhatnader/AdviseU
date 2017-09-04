from flask import Flask, flash, redirect, render_template, request, session, abort
import os


app = Flask(__name__)


@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
	username = 'admin'
	password = 'admin'

	if request.form['username'] == username and request.form['password'] == password:
		session['logged_in'] = True
	else:
		flash('Wrong username/password!')
	return redirect('/')


@app.route('/logout', methods=['POST'])
def logout():
	session['logged_in'] = False
	return redirect('/')


if __name__ == '__main__':
	app.secret_key = os.urandom(12)
	app.run(debug = True, host = '0.0.0.0', port = 8080)