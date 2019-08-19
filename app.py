from flask import Flask,flash, render_template, redirect, url_for, request, make_response
from ums import ums
import requests as rq
app = Flask(__name__)
app.secret_key = 'Hello this is a secret_key'

import mysql.connector

server = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Naman@123"
)

ums_obj = ums(server)

@app.route('/login',methods=['POST','GET'])
def login():
    error = None
    resp = make_response(render_template('login.html',error=error))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check = ums_obj.login(username, password)
        ans = str(check)
        if ans == 'True':
            flash('You are logged In')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials! Please Log In')
            return redirect(url_for('login'))
    return resp

@app.route('/register',methods=['POST','GET'])
def register():
    error = None
    resp = make_response(render_template('register.html',error=error))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check = ums_obj.register(username, password)
        if str(check)=='True':
            flash('You are now registered')
            return redirect(url_for('login'))
        else:
            flash('Invaid Credentials! Please Try Again')
            return redirect(url_for('register'))
    return resp

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    if request.method=='POST':
        if request.form['submit']=="submit":
            name = request.form['quiz_name']
            time_limit = request.form['time_limit']
            number_of_questions = request.form['number']
            print(name)
            print(time_limit)
            print(number_of_questions)
            return render_template('quiz.html')
    return render_template('dashboard.html')

@app.route('/quiz',methods=['POST','GET'])
def quiz():
    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(debug=True)
