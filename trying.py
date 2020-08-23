import sqlite3
import datetime

#history = '[(datetime.date(2020, 3, 29), "AntibioticA"), (datetime.date(2020, 3, 12), "Antibioticb")]'

conn = sqlite3.connect('tokens.db')
cur = conn.cursor()

cur.execute(f"CREATE TABLE tokens(token PRIMARY_KEY, patient_id TEXT, doctor_id TEXT, appointments TEXT, current_treatment TEXT, current_diagnosis TEXT, notifications TEXT);")
conn.commit()