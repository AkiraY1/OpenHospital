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
    
    conn = sqlite3.connect('tokens.db')
    cur = conn.cursor()
    conn1 = sqlite3.connect('users.db')
    cur1 = conn1.cursor()
    
    #Defining tokens_list
    tokens_list = []
    raw_info = cur.execute(f"SELECT * FROM tokens WHERE doctor_id = '{current_user.id}';")
    all_info = raw_info.fetchall()
    for tup in all_info:
        raw_name = cur1.execute(f"SELECT name FROM users WHERE id = '{tup[1]}'")
        name_info = raw_info.fetchone()
        tokens_list.insert(0, (tup[0], name_info))
    print(tokens_list)

    return render_template('dashboard.html', tokens_list=tokens_list)

@dash.route('/dashboard/add-patient', methods=['GET', 'POST'])
@login_required
def dashboard_add_patient():
    if current_user.role == 'Patient':
        return redirect(url_for('dashboard.dashboard_patient'))
    conn = sqlite3.connect('tokens.db')
    cur = conn.cursor()

    num = str(random.randint(1000,9999))
    new_token = generate_password_hash(num, method='md5')

    #Add into table
    new_token_info = (new_token, current_user.id)
    cur.execute("INSERT INTO tokens(token, doctor_id) VALUES(?, ?);", new_token_info)
    conn.commit()
    return redirect(url_for('dashboard.dashboard'))

@dash.route('/dashboard/join-patient', methods=['GET', 'POST'])
@login_required
def dashboard_join_patient():
    if current_user.role == 'Patient':
        return redirect(url_for('dashboard.dashboard_patient'))
    conn = sqlite3.connect('tokens.db')
    cur = conn.cursor()

    token = request.form.get('access_token')
    print(token)
    possible_raw = cur.execute(f"SELECT token FROM tokens WHERE token = '{token}';")
    possible_token = possible_raw.fetchone()
    if possible_token == None:
        flash("Token not found")
        return redirect(url_for('dashboard.dashboard'))
    else:
        new_token_info = (new_token, current_user.id)
        cur.execute("INSERT INTO tokens(token, doctor_id) VALUES(?, ?);", new_token_info)
        conn.commit()
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('dashboard.dashboard'))

#Patient Dashboard------------------------------------------------------------------------------------------

@dash.route('/dashboard-patient')
@login_required
def dashboard_patient():
    if current_user.role != 'Patient':
        return redirect(url_for('dashboard.dashboard'))
    return "Logged in successfully"