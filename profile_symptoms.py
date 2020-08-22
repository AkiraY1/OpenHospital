from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required, current_user
import sqlite3
import datetime

ps = Blueprint('ps', __name__)

@ps.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    if current_user.role == 'Doctor' or 'Nurse':
        redirect(url_for('dashboard.dashboard'))

    if current_user.treatments != None:
        treatments = ''.join(elem for elem in current_user.treatments)
        list_treatments = eval(treatments)
        list_treatments.sort(reverse=True, key=lambda x: x[0])
    else:
        list_treatments = None
    
    if current_user.diseases != None:
        diseases = ''.join(elem for elem in current_user.diseases)
        list_diseases = eval(diseases)
        list_diseases.sort(reverse=True, key=lambda x: x[0])
    else:
        list_diseases = None
    print(list_diseases)

    if request.method == 'POST':
        #import pdb
        #pdb.set_trace()
        # For changing profile
        if request.form['sub'] == 'profile':
            name = request.form.get('name')
            address = request.form.get('address')
            gender = request.form.get('gender')
            age = request.form.get('age')
            ethnicity = request.form.get('ethnicity')
            birthdate = request.form.get('birthdate')
            occupation = request.form.get('occupation')

            info_list = [('name', name), ('address', address), ('gender', gender), ('age', age), ('ethnicity', ethnicity), ('birthdate', birthdate), ('occupation', occupation)]
            for info in info_list:
                if info[1] != '':
                    cur.execute(f"UPDATE users SET {info[0]} = '{info[1]}' WHERE id = '{current_user.id}';")
                    conn.commit()
            return redirect(url_for('ps.profile', diseases=list_diseases, treatments=list_treatments))
    return render_template('profile.html', diseases=list_diseases, treatments=list_treatments)

@ps.route('/profile/add-disease', methods=['POST', 'GET'])
@login_required
def profile_add_disease():
    if request.method == 'POST':
        treatment = request.form.get('disease')
        date = request.form.get('date')
        d = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        user_id = current_user.id
        #Get current treatments list
        treatments = ''.join(elem for elem in current_user.treatments)
        list_treatments = eval(treatments)
        list_treatments.sort(reverse=True, key=lambda x: x[0])
        #Add date and name to list
        list_treatments.insert(0, (d, treatment))
        print(list_treatments)
        #Insert new list into table
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute(f'UPDATE users SET diseases = "{list_treatments}" WHERE id = "{current_user.id}";')
        conn.commit()
        current_user.diseases = list_treatments
    return redirect(url_for('ps.profile'))

@ps.route('/profile/add-treatment', methods=['POST', 'GET'])
@login_required
def profile_add_treatment():
    if request.method == 'POST':
        treatment = request.form.get('treatment')
        date = request.form.get('date')
        d = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        user_id = current_user.id
        #Get current treatments list
        treatments = ''.join(elem for elem in current_user.treatments)
        list_treatments = eval(treatments)
        list_treatments.sort(reverse=True, key=lambda x: x[0])
        #Add date and name to list
        list_treatments.insert(0, (d, treatment))
        print(list_treatments)
        #Insert new list into table
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute(f'UPDATE users SET treatments = "{list_treatments}" WHERE id = "{current_user.id}";')
        conn.commit()
        current_user.treatments = list_treatments
    return redirect(url_for('ps.profile'))

@ps.route('/profile/delete-d/<string:d>', methods=['GET', 'POST'])
@login_required
def delete_d(d):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    #Find list and fix
    diseases = ''.join(elem for elem in current_user.diseases)
    list_diseases = eval(diseases)
    list_diseases.sort(reverse=True, key=lambda x: x[0])
    
    #Find item in list and its index
    for tuples in list_diseases:
        if d in tuples:
            index = list_diseases.index(tuples)
    
    #Remove tuple from list
    list_diseases.pop(index)

    #Updating table and current_user
    cur.execute(f'UPDATE users SET diseases = "{list_diseases}" WHERE id = "{current_user.id}";')
    conn.commit()
    current_user.diseases = list_diseases

    return redirect(url_for('ps.profile'))

@ps.route('/profile/delete-t/<string:t>', methods=['GET', 'POST'])
@login_required
def delete_t(t):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    #Find list and fix
    treatments = ''.join(elem for elem in current_user.treatments)
    list_treatments = eval(treatments)
    list_treatments.sort(reverse=True, key=lambda x: x[0])
    
    #Find item in list and its index
    for tuples in list_treatments:
        if t in tuples:
            index = list_treatments.index(tuples)
    
    #Remove tuple from list
    list_treatments.pop(index)

    #Updating table and current_user
    cur.execute(f'UPDATE users SET treatments = "{list_treatments}" WHERE id = "{current_user.id}";')
    conn.commit()
    current_user.treatments = list_treatments

    return redirect(url_for('ps.profile'))