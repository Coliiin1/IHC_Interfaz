import sqlite3

try:
    db = sqlite3.connect('control_escolar.db')
    cursor = db.cursor()
    cursor.execute("UPDATE administradores SET usuario='1234567' WHERE usuario='admin123'")
    try:
        cursor.execute("ALTER TABLE materia ADD COLUMN semestre INTEGER")
    except sqlite3.OperationalError as e:
        print("Column semestre might already exist:", e)
        
    try:
        cursor.execute("ALTER TABLE materia ADD COLUMN carrera TEXT")
    except sqlite3.OperationalError as e:
        print("Column carrera might already exist in materia:", e)
        
    try:
        cursor.execute("ALTER TABLE grupo ADD COLUMN carrera TEXT")
    except sqlite3.OperationalError as e:
        print("Column carrera might already exist in grupo:", e)
        
    db.commit()
    print("Database updated successfully.")
except Exception as e:
    print("Error:", e)
finally:
    db.close()
