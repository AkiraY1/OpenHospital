from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from models import User
import random
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

dash = Blueprint('dashboard', __name__)

@dash.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Patient':
        return redirect(url_for('dashboard.dashboard_patient'))
    return render_template('dashboard.html')


@dash.route('/dashboard-patient')
@login_required
def dashboard_patient():
    if current_user.role != 'Patient':
        return redirect(url_for('dashboard.dashboard'))
    return "Logged in successfully"