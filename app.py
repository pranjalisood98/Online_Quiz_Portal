from flask import Flask,flash, render_template, redirect, url_for, request, make_response
from ums import ums
from qms import qms
import requests as rq
app = Flask(__name__)
app.secret_key = 'Hello this is a secret_key'

import mysql.connector

server = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="1234"
)

ums_obj = ums(server)
qms_obj = qms(server)
logged_in = False

@app.route('/login',methods=['POST','GET'])
def login():
    global logged_in
    logged_in = False
    error = None
    resp = make_response(render_template('login-page.html',error=error))
    if request.method == 'POST':
        if request.form['Submit'] == 'Login':
            username = request.form['username']
            password = request.form['password']
            check = ums_obj.login(username, password)
            if check:
                logged_in = True
                return redirect(url_for('dashboard'))
            else:
                flash('Either username or password is incorrect!')
                return redirect(url_for('login'))
    return resp

@app.route('/register',methods=['POST','GET'])
def register():
    error = None
    resp = make_response(render_template('register-page.html',error=error))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check = ums_obj.register(username, password)
        if str(check)=='True':
            flash('You are now registered')
            return redirect(url_for('login'))
        else:
            flash('Username already in use, please try again!')
            return redirect(url_for('register'))
    return resp

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    global logged_in
    if request.method=='POST':
        name = request.form['quiz_name']
        time_limit = request.form['time_limit']
        number_of_questions = request.form['number']
        qms_obj.create_new_paper(name, int(time_limit), int(number_of_questions))
        return redirect(url_for('quiz'))
    if not logged_in:
        return redirect(url_for('login'))
    return render_template('dashboard-page.html')

@app.route('/quiz',methods=['POST','GET'])
def quiz():
    if not logged_in:
        return redirect(url_for('login'))
    lst = []
    i = 1
    if qms_obj.num == 1:
        flash('Question paper created successfully!')
        return redirect(url_for('dashboard'))
    if request.method=='POST':
        question_description = request.form['question_description']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        answer = request.form['answer']
        lst.append(option_a)
        lst.append(option_b)
        lst.append(option_c)
        lst.append(option_d)
        qms_obj.insert_question(question_description,lst,answer)
        qms_obj.num -= 1
        i += 1
    return render_template('quiz-page.html', title=qms_obj.title, q_num=i)

if __name__ == '__main__':
    app.run(debug=True)
