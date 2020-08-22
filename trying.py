import sqlite3
import datetime

history = '[(datetime.date(2020, 3, 29), "AntibioticA"), (datetime.date(2020, 3, 12), "Antibioticb")]'

conn = sqlite3.connect('users.db')
cur = conn.cursor()

cur.execute(f"UPDATE users SET treatments = '{history}' where id = '6';")
conn.commit()