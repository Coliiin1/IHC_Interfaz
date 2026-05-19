from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import sys
import subprocess
import sqlite3

# =========================
# SISTEMA DE DISEÑO UAEMex
# =========================
C_BG        = "#F0F2F5"
C_SIDEBAR   = "#1A5C28"   # Verde institucional oscuro
C_BTN_ACT   = "#2E8B45"   # Verde activo
C_TOPBAR    = "#FFFFFF"
C_CARD      = "#FFFFFF"
C_TEXT      = "#111827"
C_MUTED     = "#6B7280"
C_BORDER    = "#E5E7EB"
C_WHITE     = "#FFFFFF"
C_BTN_TXT   = "#FFFFFF"

FONT_FAMILY = "Segoe UI"

# =========================
# ESTADO GLOBAL
# =========================
btn_activo = None

# =========================
# FUNCIONES DB
# =========================
def ejecutar_query(query, parametros=()):
    try:
        conn = sqlite3.connect('control_escolar.db')
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()
        cursor.execute(query, parametros)
        conn.commit()
        res = cursor.fetchall()
        conn.close()
        return res
    except Exception as e:
        messagebox.showerror("Error DB", str(e))
        return []

def actualizar_promedio(cuenta):
    # Calcula el nuevo promedio de un estudiante y lo actualiza
    calificaciones = ejecutar_query("SELECT AVG(calificacion) FROM calificaciones WHERE numero_de_cuenta = ?", (cuenta,))
    promedio = calificaciones[0][0] if calificaciones and calificaciones[0][0] is not None else 0.0
    ejecutar_query("UPDATE estudiante SET promedio_general = ? WHERE numero_de_cuenta = ?", (round(promedio, 2), cuenta))

# =========================
# FUNCIONES NAVEGACIÓN
# =========================
def cerrar():
    try:
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Login.py")
        subprocess.Popen([sys.executable, script])
    except: pass
    ventana.destroy()

def abrir_seccion(nombre, btn, func_render):
    global btn_activo
    if btn_activo:
        btn_activo.config(bg=C_SIDEBAR, font=(FONT_FAMILY, 10))
    btn.config(bg=C_BTN_ACT, font=(FONT_FAMILY, 10, "bold"))
    btn_activo = btn
    func_render()

# ---- Hover helpers para sidebar ----
def on_sb_enter(e, btn):
    if btn != btn_activo:
        btn.config(bg="#22703A")

def on_sb_leave(e, btn):
    if btn != btn_activo:
        btn.config(bg=C_SIDEBAR)

# =========================
# VISTAS (RENDERS)
# =========================
def limpiar_pantalla():
    for widget in area_contenido.winfo_children():
        widget.destroy()
    
    header = Frame(area_contenido, bg=C_CARD, pady=20, padx=30, highlightbackground=C_BORDER, highlightthickness=1)
    header.pack(fill=X)
    return header

def vista_dashboard():
    header = limpiar_pantalla()
    Label(header, text="Panel de Administración", font=(FONT_FAMILY, 20, "bold"), fg=C_TEXT, bg=C_CARD).pack(anchor="w")
    Label(header, text="Resumen del sistema", font=(FONT_FAMILY, 10), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    
    body = Frame(area_contenido, bg=C_BG, padx=30, pady=30)
    body.pack(expand=True, fill=BOTH)
    
    # Tarjeta de estadísticas simple
    card = Frame(body, bg=C_CARD, padx=30, pady=30, highlightbackground=C_BORDER, highlightthickness=1)
    card.pack(fill=X)
    
    estudiantes = ejecutar_query("SELECT COUNT(*) FROM estudiante")
    count = estudiantes[0][0] if estudiantes else 0
    
    Label(card, text="🎓 Estudiantes Registrados", font=(FONT_FAMILY, 14, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    Label(card, text=str(count), font=(FONT_FAMILY, 48, "bold"), fg=C_SIDEBAR, bg=C_CARD).pack(anchor="w", pady=(10, 0))

def vista_gestion_estudiantes():
    header = limpiar_pantalla()
    Label(header, text="Gestión de Estudiantes", font=(FONT_FAMILY, 20, "bold"), fg=C_TEXT, bg=C_CARD).pack(anchor="w")
    Label(header, text="Agrega o modifica a los alumnos y su carrera", font=(FONT_FAMILY, 10), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    
    body = Frame(area_contenido, bg=C_BG, padx=30, pady=30)
    body.pack(expand=True, fill=BOTH)

    # Formulario rápido
    form = Frame(body, bg=C_CARD, padx=25, pady=25, highlightbackground=C_BORDER, highlightthickness=1)
    form.pack(fill=X, pady=(0, 20))
    
    Label(form, text="Agregar / Modificar Estudiante", font=(FONT_FAMILY, 14, "bold"), fg=C_SIDEBAR, bg=C_CARD).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0,20))
    
    # Row 1
    Label(form, text="Número de Cuenta", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=0, sticky="w", pady=(0,5), padx=(0,15))
    ent_cuenta = Entry(form, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_cuenta.grid(row=2, column=0, sticky="ew", padx=(0, 15), ipady=6)
    
    Label(form, text="Nombre Completo", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=1, sticky="w", pady=(0,5), padx=(0,15))
    ent_nombre = Entry(form, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_nombre.grid(row=2, column=1, sticky="ew", padx=(0, 15), ipady=6)
    
    Label(form, text="Contraseña", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=2, sticky="w", pady=(0,5), padx=(0,15))
    ent_pass = Entry(form, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_pass.grid(row=2, column=2, sticky="ew", padx=(0, 15), ipady=6)

    Label(form, text="Carrera", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=3, sticky="w", pady=(0,5))
    
    # Obtener carreras
    carreras_db = ejecutar_query("SELECT nombre FROM carrera")
    lista_carreras = [c[0] for c in carreras_db] if carreras_db else []
    
    cb_carrera = ttk.Combobox(form, values=lista_carreras, state="readonly", font=(FONT_FAMILY, 11))
    cb_carrera.grid(row=2, column=3, sticky="ew", ipady=5)

    form.grid_columnconfigure(1, weight=1)

    def guardar():
        c, n, p, car = ent_cuenta.get(), ent_nombre.get(), ent_pass.get(), cb_carrera.get()
        if c and n and p and car:
            ejecutar_query("INSERT OR REPLACE INTO estudiante (numero_de_cuenta, nombre, contraseña, carrera, promedio_general) VALUES (?, ?, ?, ?, (SELECT COALESCE(promedio_general, 0.0) FROM estudiante WHERE numero_de_cuenta = ?))", (c, n, p, car, c))
            messagebox.showinfo("Éxito", "Estudiante guardado correctamente")
            vista_gestion_estudiantes()
        else:
            messagebox.showwarning("Error", "Completa todos los campos obligatorios.")

    btn_guardar = Button(form, text="Guardar Cambios", font=(FONT_FAMILY, 10, "bold"), command=guardar, bg=C_SIDEBAR, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_guardar.grid(row=3, column=0, columnspan=4, sticky="e", pady=(20, 0), ipadx=20, ipady=8)

    # Estilos de tabla
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=(FONT_FAMILY, 10, "bold"), background="#F9FAFB", foreground=C_MUTED, borderwidth=0)
    style.configure("Treeview", font=(FONT_FAMILY, 10), background=C_CARD, fieldbackground=C_CARD, rowheight=35, borderwidth=0)
    style.map("Treeview", background=[('selected', '#E8F5E9')], foreground=[('selected', C_SIDEBAR)])

    # Tabla de estudiantes
    tabla_frame = Frame(body, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
    tabla_frame.pack(expand=True, fill=BOTH)
    
    tree = ttk.Treeview(tabla_frame, columns=("Cuenta", "Nombre", "Carrera", "Promedio"), show="headings", style="Treeview")
    tree.heading("Cuenta", text="No. Cuenta")
    tree.heading("Nombre", text="Nombre Completo")
    tree.heading("Carrera", text="Carrera")
    tree.heading("Promedio", text="Promedio Gral.")
    
    tree.column("Cuenta", width=120, anchor="center")
    tree.column("Nombre", width=350, anchor="w")
    tree.column("Carrera", width=250, anchor="w")
    tree.column("Promedio", width=100, anchor="center")
    
    tree.pack(side=LEFT, expand=True, fill=BOTH)
    
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    estudiantes = ejecutar_query("SELECT numero_de_cuenta, nombre, carrera, promedio_general FROM estudiante")
    if estudiantes:
        for est in estudiantes:
            tree.insert("", END, values=est)

    def eliminar_seleccionado():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección Vacía", "Por favor, selecciona un alumno de la tabla para eliminarlo.")
            return
        
        item = tree.item(seleccion[0])
        cuenta_eliminar = item['values'][0]
        nombre_eliminar = item['values'][1]
        
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas dar de baja al alumno:\n{nombre_eliminar} (Cuenta: {cuenta_eliminar})?")
        if confirm:
            ejecutar_query("DELETE FROM estudiante WHERE numero_de_cuenta = ?", (str(cuenta_eliminar),))
            messagebox.showinfo("Éxito", "Alumno dado de baja correctamente.")
            vista_gestion_estudiantes()

    btn_eliminar = Button(body, text="Dar de baja seleccionado", font=(FONT_FAMILY, 10, "bold"), command=eliminar_seleccionado, bg="#DC2626", fg=C_WHITE, activebackground="#B91C1C", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_eliminar.pack(anchor="e", pady=(15, 0), ipadx=20, ipady=8)


def vista_inscripcion():
    header = limpiar_pantalla()
    Label(header, text="Inscripción de Materias", font=(FONT_FAMILY, 20, "bold"), fg=C_TEXT, bg=C_CARD).pack(anchor="w")
    Label(header, text="Inscribe a los alumnos en las materias disponibles", font=(FONT_FAMILY, 10), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    
    body = Frame(area_contenido, bg=C_BG, padx=30, pady=30)
    body.pack(expand=True, fill=BOTH)

    form = Frame(body, bg=C_CARD, padx=25, pady=25, highlightbackground=C_BORDER, highlightthickness=1)
    form.pack(fill=X, pady=(0, 20))
    
    Label(form, text="Inscribir Alumno a Materia", font=(FONT_FAMILY, 14, "bold"), fg=C_SIDEBAR, bg=C_CARD).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,20))

    estudiantes_db = ejecutar_query("SELECT numero_de_cuenta, nombre FROM estudiante")
    lista_estudiantes = [f"{e[0]} - {e[1]}" for e in estudiantes_db] if estudiantes_db else []
    
    materias_db = ejecutar_query("SELECT clave_materia, asignatura FROM materia")
    lista_materias = [f"{m[0]} - {m[1]}" for m in materias_db] if materias_db else []

    Label(form, text="Estudiante", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=0, sticky="w", pady=(0,5), padx=(0,15))
    cb_estudiante = ttk.Combobox(form, values=lista_estudiantes, state="readonly", font=(FONT_FAMILY, 11))
    cb_estudiante.grid(row=2, column=0, sticky="ew", padx=(0, 15), ipady=5)
    
    Label(form, text="Materia a inscribir", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=1, sticky="w", pady=(0,5), padx=(0,15))
    cb_materia = ttk.Combobox(form, values=[], state="readonly", font=(FONT_FAMILY, 11))
    cb_materia.grid(row=2, column=1, sticky="ew", padx=(0, 15), ipady=5)

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)

    tabla_frame = Frame(body, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
    tabla_frame.pack(expand=True, fill=BOTH)
    
    Label(tabla_frame, text="Materias Inscritas del Alumno", font=(FONT_FAMILY, 12, "bold"), fg=C_SIDEBAR, bg=C_CARD).pack(anchor="w", padx=15, pady=(15, 5))

    tree = ttk.Treeview(tabla_frame, columns=("Clave", "Materia"), show="headings", style="Treeview")
    tree.heading("Clave", text="Clave Materia")
    tree.heading("Materia", text="Asignatura")
    
    tree.column("Clave", width=150, anchor="center")
    tree.column("Materia", width=450, anchor="w")
    
    tree.pack(side=LEFT, expand=True, fill=BOTH, padx=15, pady=(0, 15))
    
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y, pady=(0, 15))

    def actualizar_tabla(event=None):
        for item in tree.get_children():
            tree.delete(item)
            
        seleccion = cb_estudiante.get()
        if not seleccion: return
        
        cuenta = seleccion.split(" - ")[0]
        historial = ejecutar_query('''
            SELECT c.clave_materia, m.asignatura
            FROM calificaciones c
            JOIN materia m ON c.clave_materia = m.clave_materia
            WHERE c.numero_de_cuenta = ?
        ''', (cuenta,))
        
        if historial:
            for row in historial:
                tree.insert("", END, values=row)

        estudiante_db = ejecutar_query("SELECT carrera FROM estudiante WHERE numero_de_cuenta = ?", (cuenta,))
        if estudiante_db and estudiante_db[0][0]:
            carrera = estudiante_db[0][0]
            materias_carrera = ejecutar_query("SELECT clave_materia, asignatura FROM materia WHERE carrera = ?", (carrera,))
            lista_materias_filtradas = [f"{m[0]} - {m[1]}" for m in materias_carrera] if materias_carrera else []
            cb_materia.config(values=lista_materias_filtradas)
            cb_materia.set("")
        else:
            cb_materia.config(values=[])
            cb_materia.set("")

    cb_estudiante.bind("<<ComboboxSelected>>", actualizar_tabla)

    def guardar_inscripcion():
        sel_est = cb_estudiante.get()
        sel_mat = cb_materia.get()
        
        if sel_est and sel_mat:
            cuenta = sel_est.split(" - ")[0]
            clave = sel_mat.split(" - ")[0]
            
            # Verificar si ya está inscrito
            existe = ejecutar_query("SELECT * FROM calificaciones WHERE numero_de_cuenta = ? AND clave_materia = ?", (cuenta, clave))
            if existe:
                messagebox.showwarning("Aviso", "El alumno ya está inscrito en esta materia.")
                return

            # Inscribir
            ejecutar_query("INSERT INTO calificaciones (numero_de_cuenta, clave_materia, calificacion) VALUES (?, ?, 0.0)", (cuenta, clave))
            
            # También lo inscribimos al grupo
            res_grupo = ejecutar_query("SELECT grupo FROM materia WHERE clave_materia = ?", (clave,))
            if res_grupo:
                ejecutar_query("INSERT OR IGNORE INTO estudiante_grupo (numero_de_cuenta, grupo) VALUES (?, ?)", (cuenta, res_grupo[0][0]))
            
            messagebox.showinfo("Éxito", "Alumno inscrito correctamente.")
            actualizar_tabla()
        else:
            messagebox.showwarning("Error", "Selecciona estudiante y materia.")

    btn_inscribir = Button(form, text="Inscribir Alumno", font=(FONT_FAMILY, 10, "bold"), command=guardar_inscripcion, bg=C_SIDEBAR, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_inscribir.grid(row=3, column=0, columnspan=2, sticky="e", pady=(20, 0), ipadx=20, ipady=8)


def vista_calificaciones():
    header = limpiar_pantalla()
    Label(header, text="Registro de Calificaciones", font=(FONT_FAMILY, 20, "bold"), fg=C_TEXT, bg=C_CARD).pack(anchor="w")
    Label(header, text="Registra las calificaciones por materia de un alumno", font=(FONT_FAMILY, 10), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    
    body = Frame(area_contenido, bg=C_BG, padx=30, pady=30)
    body.pack(expand=True, fill=BOTH)

    top_frame = Frame(body, bg=C_CARD, padx=25, pady=25, highlightbackground=C_BORDER, highlightthickness=1)
    top_frame.pack(fill=X, pady=(0, 20))
    
    Label(top_frame, text="Seleccionar Estudiante", font=(FONT_FAMILY, 14, "bold"), fg=C_SIDEBAR, bg=C_CARD).pack(anchor="w", pady=(0,10))

    estudiantes_db = ejecutar_query("SELECT numero_de_cuenta, nombre FROM estudiante")
    lista_estudiantes = [f"{e[0]} - {e[1]}" for e in estudiantes_db] if estudiantes_db else []

    cb_estudiante = ttk.Combobox(top_frame, values=lista_estudiantes, state="readonly", font=(FONT_FAMILY, 11))
    cb_estudiante.pack(fill=X, ipady=5)

    # Frame para la lista de materias (scrollable)
    list_container = Frame(body, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
    list_container.pack(expand=True, fill=BOTH)
    
    Label(list_container, text="Materias Inscritas (Calificaciones)", font=(FONT_FAMILY, 12, "bold"), fg=C_SIDEBAR, bg=C_CARD).pack(anchor="w", padx=15, pady=(15, 10))

    canvas = Canvas(list_container, bg=C_CARD, highlightthickness=0)
    scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=C_CARD)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=15, pady=(0, 15))
    scrollbar.pack(side="right", fill="y", pady=(0, 15))

    entradas_calif = {} # Diccionario para guardar clave_materia: Entry

    def actualizar_lista(event=None):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        entradas_calif.clear()
            
        seleccion = cb_estudiante.get()
        if not seleccion: return
        
        cuenta = seleccion.split(" - ")[0]
        historial = ejecutar_query('''
            SELECT c.clave_materia, m.asignatura, c.calificacion
            FROM calificaciones c
            JOIN materia m ON c.clave_materia = m.clave_materia
            WHERE c.numero_de_cuenta = ?
        ''', (cuenta,))
        
        if historial:
            for idx, row in enumerate(historial):
                clave, asig, calif = row
                
                row_frame = Frame(scrollable_frame, bg=C_CARD, pady=10)
                row_frame.pack(fill=X)
                
                Label(row_frame, text=f"{clave} - {asig}", font=(FONT_FAMILY, 11), bg=C_CARD, fg=C_TEXT, width=50, anchor="w").pack(side=LEFT, padx=(0, 20))
                
                ent = Entry(row_frame, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER, width=10, justify="center")
                ent.pack(side=LEFT, ipady=4)
                ent.insert(0, str(calif))
                
                entradas_calif[clave] = ent
        else:
            Label(scrollable_frame, text="El alumno no tiene materias inscritas.", font=(FONT_FAMILY, 11, "italic"), fg=C_MUTED, bg=C_CARD).pack(anchor="w", pady=10)

    cb_estudiante.bind("<<ComboboxSelected>>", actualizar_lista)

    def guardar_todas():
        seleccion = cb_estudiante.get()
        if not seleccion:
            messagebox.showwarning("Error", "Selecciona un estudiante.")
            return
            
        cuenta = seleccion.split(" - ")[0]
        
        for clave, ent in entradas_calif.items():
            val = ent.get().strip()
            try:
                calif_float = float(val)
                if calif_float < 0 or calif_float > 10:
                    raise ValueError
                ejecutar_query("UPDATE calificaciones SET calificacion = ? WHERE numero_de_cuenta = ? AND clave_materia = ?", (calif_float, cuenta, clave))
            except:
                messagebox.showwarning("Error", f"Calificación inválida para {clave}. Debe ser un número entre 0 y 10.")
                return
                
        # Recalcular promedio general
        actualizar_promedio(cuenta)
        messagebox.showinfo("Éxito", "Calificaciones guardadas y promedio actualizado.")
        actualizar_lista()

    bottom_frame = Frame(list_container, bg=C_CARD)
    bottom_frame.pack(fill=X, side=BOTTOM, padx=15, pady=(0, 15))
    
    btn_guardar = Button(bottom_frame, text="Guardar Todas las Calificaciones", font=(FONT_FAMILY, 10, "bold"), command=guardar_todas, bg=C_SIDEBAR, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_guardar.pack(side=RIGHT, ipadx=20, ipady=8)


def vista_gestion_carreras():
    header = limpiar_pantalla()
    Label(header, text="Gestión de Carreras", font=(FONT_FAMILY, 20, "bold"), fg=C_TEXT, bg=C_CARD).pack(anchor="w")
    Label(header, text="Agrega o elimina carreras del sistema", font=(FONT_FAMILY, 10), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    
    body = Frame(area_contenido, bg=C_BG, padx=30, pady=30)
    body.pack(expand=True, fill=BOTH)

    form = Frame(body, bg=C_CARD, padx=25, pady=25, highlightbackground=C_BORDER, highlightthickness=1)
    form.pack(fill=X, pady=(0, 20))
    
    Label(form, text="Agregar Nueva Carrera", font=(FONT_FAMILY, 14, "bold"), fg=C_SIDEBAR, bg=C_CARD).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,20))
    
    Label(form, text="Nombre de la Carrera", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=0, sticky="w", pady=(0,5), padx=(0,15))
    ent_nombre = Entry(form, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_nombre.grid(row=2, column=0, sticky="ew", padx=(0, 15), ipady=6)
    
    form.grid_columnconfigure(0, weight=1)

    def guardar():
        n = ent_nombre.get().strip()
        if n:
            ejecutar_query("INSERT OR IGNORE INTO carrera (nombre) VALUES (?)", (n,))
            messagebox.showinfo("Éxito", "Carrera guardada correctamente")
            vista_gestion_carreras()
        else:
            messagebox.showwarning("Error", "El nombre de la carrera no puede estar vacío.")

    btn_guardar = Button(form, text="Guardar Carrera", font=(FONT_FAMILY, 10, "bold"), command=guardar, bg=C_SIDEBAR, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_guardar.grid(row=2, column=1, sticky="e", ipadx=20, ipady=8)

    tabla_frame = Frame(body, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
    tabla_frame.pack(expand=True, fill=BOTH)
    
    tree = ttk.Treeview(tabla_frame, columns=("Nombre"), show="headings", style="Treeview")
    tree.heading("Nombre", text="Nombre de la Carrera")
    tree.column("Nombre", width=600, anchor="w")
    
    tree.pack(side=LEFT, expand=True, fill=BOTH)
    
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    carreras = ejecutar_query("SELECT nombre FROM carrera")
    if carreras:
        for c in carreras:
            tree.insert("", END, values=c)

    def eliminar_seleccionada():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Selección Vacía", "Por favor, selecciona una carrera de la tabla para eliminarla.")
            return
        
        item = tree.item(seleccion[0])
        nombre_eliminar = item['values'][0]
        
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar la carrera:\n{nombre_eliminar}?\n(Esto podría fallar si hay alumnos/materias/grupos asociados).")
        if confirm:
            try:
                ejecutar_query("DELETE FROM carrera WHERE nombre = ?", (nombre_eliminar,))
                messagebox.showinfo("Éxito", "Carrera eliminada correctamente.")
                vista_gestion_carreras()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la carrera. Asegúrate de que no tenga alumnos o grupos asociados.\n{e}")

    btn_eliminar = Button(body, text="Eliminar seleccionada", font=(FONT_FAMILY, 10, "bold"), command=eliminar_seleccionada, bg="#DC2626", fg=C_WHITE, activebackground="#B91C1C", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_eliminar.pack(anchor="e", pady=(15, 0), ipadx=20, ipady=8)


def vista_materias_grupos():
    header = limpiar_pantalla()
    Label(header, text="Gestión de Materias y Grupos", font=(FONT_FAMILY, 20, "bold"), fg=C_TEXT, bg=C_CARD).pack(anchor="w")
    Label(header, text="Agrega nuevos grupos y materias (Mapa Curricular)", font=(FONT_FAMILY, 10), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    
    body = Frame(area_contenido, bg=C_BG, padx=30, pady=15)
    body.pack(expand=True, fill=BOTH)

    # Contenedor superior para los dos formularios
    top_frame = Frame(body, bg=C_BG)
    top_frame.pack(fill=X, pady=(0, 15))

    # Formulario para Grupos (Mitad izquierda)
    form_grupo = Frame(top_frame, bg=C_CARD, padx=15, pady=15, highlightbackground=C_BORDER, highlightthickness=1)
    form_grupo.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
    
    Label(form_grupo, text="Agregar Nuevo Grupo", font=(FONT_FAMILY, 12, "bold"), fg=C_SIDEBAR, bg=C_CARD).pack(anchor="w", pady=(0,10))
    Label(form_grupo, text="Nombre del Grupo", font=(FONT_FAMILY, 9, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    ent_grupo = Entry(form_grupo, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_grupo.pack(fill=X, pady=(5, 10), ipady=4)
    
    Label(form_grupo, text="Carrera", font=(FONT_FAMILY, 9, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    carreras_db_g = ejecutar_query("SELECT nombre FROM carrera")
    lista_carreras_g = [c[0] for c in carreras_db_g] if carreras_db_g else []
    cb_carrera_grupo = ttk.Combobox(form_grupo, values=lista_carreras_g, state="readonly", font=(FONT_FAMILY, 10))
    cb_carrera_grupo.pack(fill=X, pady=(5, 10), ipady=2)
    
    def guardar_grupo():
        g = ent_grupo.get().strip()
        c = cb_carrera_grupo.get().strip()
        if g and c:
            ejecutar_query("INSERT OR IGNORE INTO grupo (grupo, carrera) VALUES (?, ?)", (g, c))
            messagebox.showinfo("Éxito", f"Grupo '{g}' registrado correctamente a '{c}'.")
            vista_materias_grupos()
        else:
            messagebox.showwarning("Error", "Ingresa el nombre del grupo y selecciona una carrera.")

    btn_g = Button(form_grupo, text="Guardar Grupo", font=(FONT_FAMILY, 9, "bold"), command=guardar_grupo, bg=C_SIDEBAR, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_g.pack(anchor="e", ipadx=10, ipady=4)

    # Formulario para Materias (Mitad derecha)
    form_mat = Frame(top_frame, bg=C_CARD, padx=15, pady=15, highlightbackground=C_BORDER, highlightthickness=1)
    form_mat.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
    
    Label(form_mat, text="Gestión de Materias", font=(FONT_FAMILY, 12, "bold"), fg=C_SIDEBAR, bg=C_CARD).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,10))
    
    Label(form_mat, text="Clave", font=(FONT_FAMILY, 9, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=0, sticky="w", pady=(0,2), padx=(0,5))
    ent_clave = Entry(form_mat, font=(FONT_FAMILY, 10), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_clave.grid(row=2, column=0, sticky="ew", padx=(0, 5), ipady=3)

    Label(form_mat, text="Asignatura", font=(FONT_FAMILY, 9, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=1, sticky="w", pady=(0,2), padx=(0,5))
    ent_asig = Entry(form_mat, font=(FONT_FAMILY, 10), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_asig.grid(row=2, column=1, sticky="ew", padx=(0, 5), ipady=3)

    Label(form_mat, text="Grupo", font=(FONT_FAMILY, 9, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=2, sticky="w", pady=(0,2), padx=(0,5))
    grupos_db = ejecutar_query("SELECT grupo FROM grupo")
    lista_grupos = [g[0] for g in grupos_db] if grupos_db else []
    cb_grupo = ttk.Combobox(form_mat, values=lista_grupos, state="readonly", font=(FONT_FAMILY, 10), width=8)
    cb_grupo.grid(row=2, column=2, sticky="ew", padx=(0, 5), ipady=2)

    Label(form_mat, text="Semestre", font=(FONT_FAMILY, 9, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=3, column=0, sticky="w", pady=(10,2), padx=(0,5))
    cb_sem = ttk.Combobox(form_mat, values=[str(i) for i in range(1, 11)], state="readonly", font=(FONT_FAMILY, 10), width=8)
    cb_sem.grid(row=4, column=0, sticky="ew", padx=(0, 5), ipady=2)

    Label(form_mat, text="Carrera", font=(FONT_FAMILY, 9, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=3, column=1, columnspan=2, sticky="w", pady=(10,2), padx=(0,5))
    carreras_db = ejecutar_query("SELECT nombre FROM carrera")
    lista_carreras = [c[0] for c in carreras_db] if carreras_db else []
    cb_carrera_mat = ttk.Combobox(form_mat, values=lista_carreras, state="readonly", font=(FONT_FAMILY, 10))
    cb_carrera_mat.grid(row=4, column=1, columnspan=2, sticky="ew", padx=(0, 5), ipady=2)

    form_mat.grid_columnconfigure(1, weight=1)

    def guardar_materia():
        c = ent_clave.get().strip()
        a = ent_asig.get().strip()
        g = cb_grupo.get().strip()
        s = cb_sem.get().strip()
        car = cb_carrera_mat.get().strip()
        if c and a and g and s and car:
            ejecutar_query("INSERT OR REPLACE INTO materia (clave_materia, asignatura, grupo, semestre, carrera) VALUES (?, ?, ?, ?, ?)", (c, a, g, int(s), car))
            messagebox.showinfo("Éxito", f"Materia '{a}' registrada correctamente.")
            vista_materias_grupos()
        else:
            messagebox.showwarning("Error", "Completa todos los campos.")

    def borrar_materia():
        c = ent_clave.get().strip()
        if c:
            respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de borrar la materia con clave '{c}'?")
            if respuesta:
                ejecutar_query("DELETE FROM materia WHERE clave_materia = ?", (c,))
                messagebox.showinfo("Éxito", f"Materia '{c}' eliminada.")
                vista_materias_grupos()
        else:
            messagebox.showwarning("Error", "Ingresa la clave de la materia a borrar.")

    btn_m = Button(form_mat, text="Guardar Materia", font=(FONT_FAMILY, 9, "bold"), command=guardar_materia, bg=C_SIDEBAR, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_m.grid(row=5, column=2, sticky="e", pady=(10, 0), ipadx=10, ipady=4)
    
    btn_b_m = Button(form_mat, text="Borrar", font=(FONT_FAMILY, 9, "bold"), command=borrar_materia, bg="#DC2626", fg=C_WHITE, activebackground="#991B1B", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_b_m.grid(row=5, column=1, sticky="e", pady=(10, 0), padx=(0, 5), ipadx=10, ipady=4)

    def cargar_mapa_pdf():
        car = cb_carrera_mat.get().strip()
        g = cb_grupo.get().strip()
        if not car or not g:
            messagebox.showwarning("Faltan datos", "Por favor, selecciona una 'Carrera' y un 'Grupo' base en el formulario de arriba.")
            return
            
        archivo = filedialog.askopenfilename(title="Seleccionar Mapa Curricular (PDF)", filetypes=[("Archivos PDF", "*.pdf")])
        if not archivo: return
        
        try:
            import pdfplumber
            import re
            materias_agregadas = 0
            with pdfplumber.open(archivo) as pdf:
                for page in pdf.pages:
                    words = page.extract_words()
                    if not words: continue
                    
                    # 1. Encontrar encabezados de periodo
                    period_x = []
                    for w in words:
                        m = re.search(r'(?i)periodo\s*_?\s*(\d+)', w['text'])
                        if m:
                            period_x.append((int(m.group(1)), (w['x0'] + w['x1']) / 2))
                            
                    if period_x:
                        # Parsing visual basado en coordenadas (para diagramas de flujo/cajas)
                        period_x.sort(key=lambda x: x[1])
                        
                        def get_closest_sem(wx):
                            min_dist = float('inf')
                            closest = None
                            for sem, px in period_x:
                                dist = abs(wx - px)
                                if dist < min_dist:
                                    min_dist = dist
                                    closest = sem
                            return closest
                            
                        # Agrupar palabras por semestre
                        words_by_sem = {sem: [] for sem, _ in period_x}
                        for w in words:
                            text = w['text'].strip()
                            if re.search(r'(?i)periodo\s*_?\s*\d+', text): continue
                            if re.search(r'^\(?\d+(\.\d+)?\)?$', text): continue # Ignorar numeros sueltos o creditos como (8.0)
                            
                            wx = (w['x0'] + w['x1']) / 2
                            sem = get_closest_sem(wx)
                            if sem is not None:
                                words_by_sem[sem].append(w)
                                
                        for sem, sem_words in words_by_sem.items():
                            if not sem_words: continue
                            # Ordenar palabras de arriba a abajo, izq a der. round a 5 para misma linea
                            sem_words.sort(key=lambda w: (round(w['top'] / 5) * 5, w['x0']))
                            
                            current_subject = []
                            last_bottom = -100
                            
                            for w in sem_words:
                                if current_subject and (w['top'] - last_bottom > 12):
                                    materia = " ".join(current_subject).strip()
                                    if materia:
                                        iniciales = "".join([p[:2].upper() for p in materia.split() if len(p)>2])
                                        clave = f"{car[:3].upper()}-{sem}-{iniciales}"[:15]
                                        ejecutar_query("INSERT OR IGNORE INTO materia (clave_materia, asignatura, grupo, semestre, carrera) VALUES (?, ?, ?, ?, ?)", (clave, materia, g, int(sem), car))
                                        materias_agregadas += 1
                                    current_subject = []
                                
                                current_subject.append(w['text'])
                                last_bottom = max(last_bottom, w['bottom'])
                                
                            if current_subject:
                                materia = " ".join(current_subject).strip()
                                if materia:
                                    iniciales = "".join([p[:2].upper() for p in materia.split() if len(p)>2])
                                    clave = f"{car[:3].upper()}-{sem}-{iniciales}"[:15]
                                    ejecutar_query("INSERT OR IGNORE INTO materia (clave_materia, asignatura, grupo, semestre, carrera) VALUES (?, ?, ?, ?, ?)", (clave, materia, g, int(sem), car))
                                    materias_agregadas += 1
                    else:
                        # Fallback a texto o tablas
                        tables = page.extract_tables()
                        if tables:
                            for table in tables:
                                for row in table:
                                    row_limpia = [str(c).strip() for c in row if c is not None and str(c).strip() != ""]
                                    if len(row_limpia) >= 2:
                                        semestre = ""
                                        materia = ""
                                        for celda in row_limpia:
                                            if celda.isdigit() and len(celda) <= 2:
                                                semestre = celda
                                            elif not materia and not celda.lower() in ["semestre", "asignatura", "materia", "nombre"]:
                                                materia = celda
                                        if materia and semestre:
                                            materia = materia.replace('\n', ' ').strip()
                                            iniciales = "".join([p[:2].upper() for p in materia.split() if len(p)>2])
                                            clave = f"{car[:3].upper()}-{semestre}-{iniciales}"[:15]
                                            ejecutar_query("INSERT OR IGNORE INTO materia (clave_materia, asignatura, grupo, semestre, carrera) VALUES (?, ?, ?, ?, ?)", (clave, materia, g, int(semestre), car))
                                            materias_agregadas += 1
                        else:
                            text = page.extract_text()
                            if text:
                                for line in text.split('\n'):
                                    line = line.strip()
                                    if not line: continue
                                    match_al_final = re.search(r'^(.*?)\s+(\d{1,2})$', line)
                                    match_al_inicio = re.search(r'^(\d{1,2})\s+(.*?)$', line)
                                    materia = ""
                                    semestre = ""
                                    if match_al_final:
                                        materia, semestre = match_al_final.groups()
                                    elif match_al_inicio:
                                        semestre, materia = match_al_inicio.groups()
                                    
                                    if materia and semestre and not "semestre" in materia.lower():
                                        iniciales = "".join([p[:2].upper() for p in materia.split() if len(p)>2])
                                        clave = f"{car[:3].upper()}-{semestre}-{iniciales}"[:15]
                                        ejecutar_query("INSERT OR IGNORE INTO materia (clave_materia, asignatura, grupo, semestre, carrera) VALUES (?, ?, ?, ?, ?)", (clave, materia, g, int(semestre), car))
                                        materias_agregadas += 1

            if materias_agregadas > 0:
                messagebox.showinfo("Éxito", f"Se registraron {materias_agregadas} materias desde el PDF.")
                vista_materias_grupos()
            else:
                messagebox.showwarning("Sin resultados", "No se detectó ninguna materia/semestre en el formato esperado.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar el PDF:\n{e}")

    btn_pdf = Button(form_mat, text="📄 Cargar PDF (Mapa Curricular)", font=(FONT_FAMILY, 9, "bold"), command=cargar_mapa_pdf, bg="#4F46E5", fg=C_WHITE, activebackground="#4338CA", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_pdf.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0), ipadx=10, ipady=4)

    # Tabla Mapa Curricular
    tabla_frame = Frame(body, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
    tabla_frame.pack(expand=True, fill=BOTH)
    
    Label(tabla_frame, text="Mapa Curricular (Materias)", font=(FONT_FAMILY, 12, "bold"), fg=C_SIDEBAR, bg=C_CARD).pack(anchor="w", padx=15, pady=(15, 5))
    
    tree = ttk.Treeview(tabla_frame, columns=("Carrera", "Semestre", "Clave", "Asignatura", "Grupo"), show="headings", style="Treeview")
    tree.heading("Carrera", text="Carrera")
    tree.heading("Semestre", text="Semestre")
    tree.heading("Clave", text="Clave")
    tree.heading("Asignatura", text="Asignatura")
    tree.heading("Grupo", text="Grupo")
    
    tree.column("Carrera", width=250, anchor="w")
    tree.column("Semestre", width=80, anchor="center")
    tree.column("Clave", width=100, anchor="center")
    tree.column("Asignatura", width=300, anchor="w")
    tree.column("Grupo", width=80, anchor="center")
    
    tree.pack(side=LEFT, expand=True, fill=BOTH, padx=15, pady=(0, 15))
    
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y, pady=(0, 15))

    materias_lista = ejecutar_query("SELECT carrera, semestre, clave_materia, asignatura, grupo FROM materia ORDER BY carrera, semestre, asignatura")
    if materias_lista:
        for m in materias_lista:
            m_fixed = [str(x) if x is not None else "N/A" for x in m]
            tree.insert("", END, values=m_fixed)

    def on_tree_select(event):
        seleccion = tree.selection()
        if not seleccion: return
        item = tree.item(seleccion[0])
        valores = item['values']
        if valores:
            ent_clave.delete(0, END)
            ent_clave.insert(0, valores[2])
            
            ent_asig.delete(0, END)
            ent_asig.insert(0, valores[3])
            
            cb_grupo.set(valores[4])
            cb_sem.set(valores[1])
            cb_carrera_mat.set(valores[0])

    tree.bind("<<TreeviewSelect>>", on_tree_select)


# =========================
# DATOS DE USUARIO
# =========================
usuario_cuenta = sys.argv[1] if len(sys.argv) > 1 else "1234567"
usuario_nombre = sys.argv[2] if len(sys.argv) > 2 else "Administrador General"

partes = usuario_nombre.split()
iniciales = "".join(p[0] for p in partes[:2]).upper() if partes else "A"

# =========================
# VENTANA PRINCIPAL
# =========================
ventana = Tk()
ventana.geometry("1100x700")
ventana.title("Panel Administrador — UAEMex")
ventana.config(bg=C_BG)

# TOPBAR
topbar = Frame(ventana, bg=C_TOPBAR, height=60, highlightbackground=C_BORDER, highlightthickness=1)
topbar.pack(side=TOP, fill=X)
topbar.pack_propagate(False)

Label(topbar, text="MODO ADMINISTRADOR", font=(FONT_FAMILY, 12, "bold"), fg="#B91C1C", bg=C_TOPBAR).pack(side=LEFT, padx=24)

# Info del usuario (derecha)
user_frame = Frame(topbar, bg=C_TOPBAR)
user_frame.pack(side=RIGHT, padx=24)

avatar = Frame(user_frame, bg=C_SIDEBAR, width=36, height=36)
avatar.pack(side=LEFT, padx=(0, 8))
avatar.pack_propagate(False)
Label(avatar, text=iniciales, font=(FONT_FAMILY, 11, "bold"),
      fg=C_WHITE, bg=C_SIDEBAR).place(relx=0.5, rely=0.5, anchor="center")

Label(
    user_frame,
    text=usuario_nombre,
    font=(FONT_FAMILY, 11, "bold"),
    fg=C_TEXT,
    bg=C_TOPBAR
).pack(side=LEFT)

Label(
    user_frame,
    text="Admin",
    font=(FONT_FAMILY, 9),
    fg=C_MUTED,
    bg=C_TOPBAR
).pack(side=LEFT, padx=(6, 0))

# CUERPO
cuerpo = Frame(ventana, bg=C_BG)
cuerpo.pack(expand=True, fill=BOTH)

# SIDEBAR
sidebar = Frame(cuerpo, bg=C_SIDEBAR, width=220)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)

Label(sidebar, text="ADMINISTRACIÓN", font=(FONT_FAMILY, 8, "bold"), fg="#6BBF80", bg=C_SIDEBAR).pack(anchor="w", padx=18, pady=(20, 10))

# Botones Sidebar
btn_dash = Button(sidebar, text="📊 Dashboard", font=(FONT_FAMILY, 10), fg=C_WHITE, bg=C_SIDEBAR, bd=0, anchor="w", padx=18, cursor="hand2")
btn_dash.pack(fill=X, ipady=12)
btn_dash.config(command=lambda: abrir_seccion("Dashboard", btn_dash, vista_dashboard))
btn_dash.bind("<Enter>", lambda e: on_sb_enter(e, btn_dash))
btn_dash.bind("<Leave>", lambda e: on_sb_leave(e, btn_dash))

btn_gest = Button(sidebar, text="👥 Gestionar Alumnos", font=(FONT_FAMILY, 10), fg=C_WHITE, bg=C_SIDEBAR, bd=0, anchor="w", padx=18, cursor="hand2")
btn_gest.pack(fill=X, ipady=12)
btn_gest.config(command=lambda: abrir_seccion("Gestión", btn_gest, vista_gestion_estudiantes))
btn_gest.bind("<Enter>", lambda e: on_sb_enter(e, btn_gest))
btn_gest.bind("<Leave>", lambda e: on_sb_leave(e, btn_gest))

btn_carreras = Button(sidebar, text="🎓 Gestionar Carreras", font=(FONT_FAMILY, 10), fg=C_WHITE, bg=C_SIDEBAR, bd=0, anchor="w", padx=18, cursor="hand2")
btn_carreras.pack(fill=X, ipady=12)
btn_carreras.config(command=lambda: abrir_seccion("Carreras", btn_carreras, vista_gestion_carreras))
btn_carreras.bind("<Enter>", lambda e: on_sb_enter(e, btn_carreras))
btn_carreras.bind("<Leave>", lambda e: on_sb_leave(e, btn_carreras))

btn_inscribir = Button(sidebar, text="📌 Inscribir Materia", font=(FONT_FAMILY, 10), fg=C_WHITE, bg=C_SIDEBAR, bd=0, anchor="w", padx=18, cursor="hand2")
btn_inscribir.pack(fill=X, ipady=12)
btn_inscribir.config(command=lambda: abrir_seccion("Inscripciones", btn_inscribir, vista_inscripcion))
btn_inscribir.bind("<Enter>", lambda e: on_sb_enter(e, btn_inscribir))
btn_inscribir.bind("<Leave>", lambda e: on_sb_leave(e, btn_inscribir))

btn_calif = Button(sidebar, text="📝 Calificaciones", font=(FONT_FAMILY, 10), fg=C_WHITE, bg=C_SIDEBAR, bd=0, anchor="w", padx=18, cursor="hand2")
btn_calif.pack(fill=X, ipady=12)
btn_calif.config(command=lambda: abrir_seccion("Calificaciones", btn_calif, vista_calificaciones))
btn_calif.bind("<Enter>", lambda e: on_sb_enter(e, btn_calif))
btn_calif.bind("<Leave>", lambda e: on_sb_leave(e, btn_calif))

btn_mat = Button(sidebar, text="📚 Materias y Grupos", font=(FONT_FAMILY, 10), fg=C_WHITE, bg=C_SIDEBAR, bd=0, anchor="w", padx=18, cursor="hand2")
btn_mat.pack(fill=X, ipady=12)
btn_mat.config(command=lambda: abrir_seccion("Materias y Grupos", btn_mat, vista_materias_grupos))
btn_mat.bind("<Enter>", lambda e: on_sb_enter(e, btn_mat))
btn_mat.bind("<Leave>", lambda e: on_sb_leave(e, btn_mat))


btn_cerrar = Button(sidebar, text="⏻ Cerrar Sesión", font=(FONT_FAMILY, 10), fg="#F87171", bg=C_SIDEBAR, bd=0, anchor="w", padx=18, cursor="hand2", command=cerrar)
btn_cerrar.pack(fill=X, ipady=12, side=BOTTOM)
btn_cerrar.bind("<Enter>", lambda e: btn_cerrar.config(bg="#7F1D1D", fg=C_WHITE))
btn_cerrar.bind("<Leave>", lambda e: btn_cerrar.config(bg=C_SIDEBAR, fg="#F87171"))

# ÁREA DE CONTENIDO
area_contenido = Frame(cuerpo, bg=C_BG)
area_contenido.pack(side=RIGHT, expand=True, fill=BOTH)

# Carga inicial
abrir_seccion("Dashboard", btn_dash, vista_dashboard)

ventana.mainloop()
