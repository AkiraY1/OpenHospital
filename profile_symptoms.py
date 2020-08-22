from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import login_required, current_user
import sqlite3
import datetime
from symptoms import PROBLEMS
import requests

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

# -------------------------------------------------------------------------------------------------------------------------------

@ps.route('/symptoms', methods=['GET', 'POST'])
@login_required
def symptoms():
    if current_user.symptoms != None:
        symptoms = ''.join(elem for elem in current_user.symptoms)
        list_symptoms = eval(symptoms)
    else:
        list_symptoms = None

    #MED API ---------------------------------------------------------------------------------------
    #symptoms_list = []
    #for tup in list_symptoms:
    #    symptoms_list.append(int(tup[0]))
    #current_user.gender = 'male'
    #urrent_user.age = 40
    #print(symptoms_list)
    #req = requests.get(f'https://healthservice.priaid.ch/diagnosis?symptoms={symptoms_list}&gender={current_user.gender}&year_of_birth={current_user.age}&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Imx1Y2t5YW5jaG9yMkBnbWFpbC5jb20iLCJyb2xlIjoiVXNlciIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3NpZCI6IjQ5ODQiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3ZlcnNpb24iOiIxMDkiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xpbWl0IjoiMTAwIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwIjoiQmFzaWMiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xhbmd1YWdlIjoiZW4tZ2IiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDk5LTEyLTMxIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwc3RhcnQiOiIyMDIwLTA4LTIxIiwiaXNzIjoiaHR0cHM6Ly9hdXRoc2VydmljZS5wcmlhaWQuY2giLCJhdWQiOiJodHRwczovL2hlYWx0aHNlcnZpY2UucHJpYWlkLmNoIiwiZXhwIjoxNTk4MDg1OTI4LCJuYmYiOjE1OTgwNzg3Mjh9.2z8tJEFtMUVgUBjHsLOb3g1-2BDoTbELZnXHIrLWsc4&format=json&language=en-gb')
    #print(req.json())

    if request.method == 'POST':
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        value = request.form.get('symptom')
        
        #Find value in PROBLEMS
        for dic in PROBLEMS:
            values = dic.values()
            if value in values:
                list_values = list(values)
                code = list_values[0]

        #Create new list with current values
        symptoms = ''.join(elem for elem in current_user.symptoms)
        current_symptoms = eval(symptoms)
        current_symptoms.insert(0, (code, value))

        #Add value to table and current_user
        cur.execute(f'UPDATE users SET symptoms = "{current_symptoms}" WHERE id = "{current_user.id}";')
        conn.commit()
        current_user.symptoms = current_symptoms
        return redirect(url_for('ps.symptoms'))

    return render_template('symptoms.html', PROBLEMS=PROBLEMS, symptoms=list_symptoms)

@ps.route('/symptoms/delete-s/<string:s>', methods=['GET', 'POST'])
@login_required
def delete_s(s):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    #Find list and fix
    symptoms = ''.join(elem for elem in current_user.symptoms)
    list_symptoms = eval(symptoms)
    
    #Find item in list and its index
    for tuples in list_symptoms:
        if s in tuples:
            index = list_symptoms.index(tuples)
    
    #Remove tuple from list
    list_symptoms.pop(index)

    #Updating table and current_user
    cur.execute(f'UPDATE users SET symptoms = "{list_symptoms}" WHERE id = "{current_user.id}";')
    conn.commit()
    current_user.symptoms = list_symptoms

    return redirect(url_for('ps.symptoms'))