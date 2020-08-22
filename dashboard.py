from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from models import User
import random
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import datetime

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
    raw_info = cur.execute(f"SELECT * FROM tokens;")
    all_info = raw_info.fetchall()
    print(all_info)
    for tup in all_info:
        idees = ''.join(elem for elem in tup[2])
        list_of_idees = eval(idees)
        print(list_of_idees)
        if current_user.id in list_of_idees:
            raw_name = cur1.execute(f"SELECT name FROM users WHERE id = '{tup[1]}'")
            print(tup[1])
            name_info = raw_name.fetchone()
            print(name_info)
            if name_info != None:
                tokens_list.insert(0, (tup[0], str(name_info).strip("(),'")))
            else:
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
    new_token_info = [current_user.id]
    print(new_token_info)
    cur.execute(f"INSERT INTO tokens(token, doctor_id, apointments, current_treatment, current_diagnosis, notifications) VALUES('{new_token}', '{new_token_info}', '[]', '[]','[]','[]');")
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
    possible_raw = cur.execute(f"SELECT * FROM tokens WHERE token = '{token}';")
    possible_token = possible_raw.fetchone()
    if possible_token == None:
        flash("Token not found")
        return redirect(url_for('dashboard.dashboard'))
    else:
        doctor_id_list = []
        ids_list = ''.join(elem for elem in possible_token[2])
        list_of_ids = eval(ids_list)
        for idy in list_of_ids:
            doctor_id_list.append(idy)
        doctor_id_list.append(current_user.id)
        print(doctor_id_list)
        cur.execute(f'UPDATE tokens SET doctor_id = "{doctor_id_list}" WHERE token = "{possible_token[0]}";')
        conn.commit()
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('dashboard.dashboard'))

@dash.route('/dashboard/<string:token>', methods=['GET', 'POST'])
@login_required
def dashboard_view_patient(token):
    conn = sqlite3.connect('tokens.db')
    cur = conn.cursor()
    conn1 = sqlite3.connect('users.db')
    cur1 = conn1.cursor()

    raw_token_info = cur.execute(f"SELECT patient_id, appointments, current_treatment, current_diagnosis, notifications FROM tokens WHERE token = '{token}';")
    token_info = raw_token_info.fetchone()
    raw_user_info = cur1.execute(f"SELECT * FROM users WHERE id = '{token_info[0]}';")
    user_info = raw_user_info.fetchone()

    #Add the token db information into a new list
    token_info_list = [token_info, user_info]
    print(token_info_list)
    
    #Create history diseases list
    listy_diseases = ''.join(elem for elem in token_info_list[1][15])
    diseases_list = eval(listy_diseases)

    #Create history treatments list
    listy_treatments = ''.join(elem for elem in token_info_list[1][14])
    treatments_list = eval(listy_treatments)

    #Create symptoms list
    listy_symptoms = ''.join(elem for elem in token_info_list[1][12])
    symptoms_list = eval(listy_symptoms)

    #Create diagnosis list
    listy_diagnosis = ''.join(elem for elem in token_info_list[0][3])
    diagnosis_list = eval(listy_diagnosis)

    #Create treatments list
    current_listy_treatments = ''.join(elem for elem in token_info_list[0][2])
    current_treatments_list = eval(current_listy_treatments)
    
    #Create whole appointments list
    listy_appointments = ''.join(elem for elem in token_info_list[0][1])
    appointments_list = eval(listy_appointments)

    #Create appointments list
    #listy_appointments = ''.join(elem for elem in token_info_list[0][1])
    #appointments_list = eval(listy_appointments)

    ##Create requested appointments list
    #rlisty_appointments = ''.join(elem for elem in token_info_list[0][1])
    #rappointments_list = eval(rlisty_appointments)

    return render_template('dashboard_view_patient.html', diseases=diseases_list, treatments=treatments_list, symptoms=symptoms_list, diagnosis=diagnosis_list, current_treatments=current_treatments_list, appointments=appointments_list)

#Delete appointment requests
@dash.route('/dashboard/delete-ra/<string:content>', methods=['GET', 'POST'])
@login_required
def delete_ra(content):
    conn = sqlite3.connect('tokens.db')
    cur = conn.cursor()

    cur.execute()

    return redirect(url_for('dashboard.dashboard'))

#Accept appointment requests
@dash.route('/dashboard/accept-ra/<string:content>', methods=['GET', 'POST'])
@login_required
def accept_ra(content):
    print(content)
    return redirect(url_for('dashboard.dashboard'))

#Patient Dashboard------------------------------------------------------------------------------------------

@dash.route('/dashboard-patient')
@login_required
def dashboard_patient():
    if current_user.role != 'Patient':
        return redirect(url_for('dashboard.dashboard'))
    return "Logged in successfully"