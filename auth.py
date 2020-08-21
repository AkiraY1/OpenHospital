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
        return redirect(url_for('auth.welcome'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['GET', 'POST'])
def login_post():
    return "Login-post"