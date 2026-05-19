import sqlite3

def init_db():
    conn = sqlite3.connect('control_escolar.db')
    
    # Habilitar el soporte para llaves foráneas en SQLite
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()

    # Eliminar tablas antiguas si existen (Cuidado: esto borra los datos anteriores)
    cursor.execute('DROP TABLE IF EXISTS usuarios')
    cursor.execute('DROP TABLE IF EXISTS calificaciones')
    cursor.execute('DROP TABLE IF EXISTS estudiante_grupo')
    cursor.execute('DROP TABLE IF EXISTS materia')
    cursor.execute('DROP TABLE IF EXISTS estudiante')
    cursor.execute('DROP TABLE IF EXISTS grupo')
    cursor.execute('DROP TABLE IF EXISTS carrera')
    cursor.execute('DROP TABLE IF EXISTS administradores')

    # 1. Tabla Administradores
    cursor.execute('''
        CREATE TABLE administradores (
            usuario TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL
        )
    ''')

    # 2. Tabla Carrera
    cursor.execute('''
        CREATE TABLE carrera (
            nombre TEXT PRIMARY KEY
        )
    ''')

    # 3. Tabla Grupo
    cursor.execute('''
        CREATE TABLE grupo (
            grupo TEXT PRIMARY KEY,
            carrera TEXT,
            FOREIGN KEY(carrera) REFERENCES carrera(nombre) ON DELETE CASCADE
        )
    ''')

    # 4. Tabla Materia
    cursor.execute('''
        CREATE TABLE materia (
            clave_materia TEXT PRIMARY KEY,
            asignatura TEXT NOT NULL,
            grupo TEXT,
            FOREIGN KEY(grupo) REFERENCES grupo(grupo) ON DELETE CASCADE
        )
    ''')

    # 5. Tabla Estudiante
    cursor.execute('''
        CREATE TABLE estudiante (
            numero_de_cuenta TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            contraseña TEXT NOT NULL,
            carrera TEXT,
            promedio_general REAL DEFAULT 0.0,
            FOREIGN KEY(carrera) REFERENCES carrera(nombre) ON DELETE SET NULL
        )
    ''')

    # 6. Tabla Estudiante_Grupo (Inscripción a grupos)
    cursor.execute('''
        CREATE TABLE estudiante_grupo (
            numero_de_cuenta TEXT,
            grupo TEXT,
            PRIMARY KEY (numero_de_cuenta, grupo),
            FOREIGN KEY(numero_de_cuenta) REFERENCES estudiante(numero_de_cuenta) ON DELETE CASCADE,
            FOREIGN KEY(grupo) REFERENCES grupo(grupo) ON DELETE CASCADE
        )
    ''')

    # 7. Tabla Calificaciones (Para asignar promedio por materia a un alumno)
    cursor.execute('''
        CREATE TABLE calificaciones (
            numero_de_cuenta TEXT,
            clave_materia TEXT,
            calificacion REAL DEFAULT 0.0,
            PRIMARY KEY (numero_de_cuenta, clave_materia),
            FOREIGN KEY(numero_de_cuenta) REFERENCES estudiante(numero_de_cuenta) ON DELETE CASCADE,
            FOREIGN KEY(clave_materia) REFERENCES materia(clave_materia) ON DELETE CASCADE
        )
    ''')

    # =========================
    # INSERTAR DATOS DE PRUEBA
    # =========================
    
    # Administrador
    cursor.execute("INSERT INTO administradores VALUES ('admin123', 'admin789', 'Administrador General')")
    
    # Carreras
    cursor.execute("INSERT INTO carrera VALUES ('Ingeniería en Computación')")
    cursor.execute("INSERT INTO carrera VALUES ('Ingeniería en Software')")
    
    # Grupos
    cursor.execute("INSERT INTO grupo VALUES ('ICO-01', 'Ingeniería en Computación')")
    cursor.execute("INSERT INTO grupo VALUES ('ISO-02', 'Ingeniería en Software')")
    
    # Materias
    cursor.executemany("INSERT INTO materia VALUES (?, ?, ?)", [
        ('MAT-101', 'Cálculo Diferencial', 'ICO-01'),
        ('PRO-101', 'Programación Básica', 'ICO-01'),
        ('BD-201', 'Bases de Datos', 'ISO-02')
    ])
    
    # Estudiante
    cursor.execute("INSERT INTO estudiante VALUES ('1234567', 'Juan Pérez Sánchez', 'pass123', 'Ingeniería en Computación', 8.5)")
    
    # Inscripción a grupo
    cursor.execute("INSERT INTO estudiante_grupo VALUES ('1234567', 'ICO-01')")
    
    # Calificaciones
    cursor.executemany("INSERT INTO calificaciones VALUES (?, ?, ?)", [
        ('1234567', 'MAT-101', 8.0),
        ('1234567', 'PRO-101', 9.0)
    ])

    conn.commit()
    conn.close()
    print("Base de datos estructurada e inicializada correctamente (control_escolar.db)")

if __name__ == "__main__":
    init_db()
