from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from models import User

auth = Blueprint('auth', __name__)

@auth.route('/')
def welcome():
    return render_template('welcome.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    role = request.form.get('role')
    practice = request.form.get('practice')

    if (email == None) or (password == None) or (practice == None) or (name == None) or (role == None):
        flash("Please fill every field")
        return redirect(url_for('auth.signup'))

    check_email = cur.execute(f"SELECT email FROM users WHERE email = '{email}';")
    email_result = check_email.fetchone()

    if email_result != None:
        flash("Email already signed up")
        return redirect(url_for('auth.signup'))

    else:
        cur.execute(f"INSERT INTO users(email, name, password, role, practice) VALUES('{email}','{name}','{generate_password_hash(password, method='sha256')}','{role}','{practice}');")
        conn.commit()
        idy = cur.execute(f"SELECT id FROM users WHERE email = '{email}';")
        user_id = idy.fetchone()
        new_user = User(user_id, email, name, password, role, practice, None, None, None, None, None, None, None, None)
        login_user(new_user)
        return redirect(url_for('dashboard.dashboard'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['GET', 'POST'])
def login_post():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    email = request.form.get('email')
    password = request.form.get('password')

    if (email == None) or (password == None):
        flash("Please fill every field")
        return redirect(url_for('auth.signup'))

    user_info = cur.execute(f"SELECT * FROM users WHERE email = '{email}';")
    user_info_fetched = user_info.fetchone()

    if user_info_fetched[0] == None:
        flash("This email is not signed up yet")
        return redirect(url_for('auth.login'))
    
    if check_password_hash(user_info_fetched[3], password):
        user = User(user_info_fetched[0], user_info_fetched[1], user_info_fetched[2], user_info_fetched[3], user_info_fetched[4], user_info_fetched[5], user_info_fetched[6], user_info_fetched[7], user_info_fetched[8], user_info_fetched[9], user_info_fetched[10], user_info_fetched[11], user_info_fetched[12], user_info_fetched[13])
        login_user(user)
        return redirect(url_for('dashboard.dashboard'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.welcome'))