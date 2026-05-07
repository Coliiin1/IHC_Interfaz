import sqlite3

def init_db():
    # Conectar (se crea el archivo si no existe)
    conn = sqlite3.connect('control_escolar.db')
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            num_cuenta TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
            rol TEXT DEFAULT 'Estudiante'
        )
    ''')

    # Insertar usuarios de prueba
    usuarios = [
        ('1234567', 'pass123', 'Juan Pérez Sánchez', 'Estudiante'),
        ('admin123', 'admin789', 'Administrador General', 'Admin')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO usuarios (num_cuenta, password, nombre, rol)
        VALUES (?, ?, ?, ?)
    ''', usuarios)

    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente (control_escolar.db)")

if __name__ == "__main__":
    init_db()
