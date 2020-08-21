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

@auth.route('/signup')
def signup_post():
    return "Signup-post"

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login')
def login_post():
    return "Login-post"