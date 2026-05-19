import sqlite3
db = sqlite3.connect('control_escolar.db')
cursor = db.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
for row in cursor.fetchall():
    if row[0]:
        print(row[0])
