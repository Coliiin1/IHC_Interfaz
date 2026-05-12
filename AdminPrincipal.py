from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
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


def vista_calificaciones():
    header = limpiar_pantalla()
    Label(header, text="Calificaciones e Inscripciones", font=(FONT_FAMILY, 20, "bold"), fg=C_TEXT, bg=C_CARD).pack(anchor="w")
    Label(header, text="Asigna materias y calificaciones a los alumnos", font=(FONT_FAMILY, 10), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    
    body = Frame(area_contenido, bg=C_BG, padx=30, pady=30)
    body.pack(expand=True, fill=BOTH)

    # Formulario
    form = Frame(body, bg=C_CARD, padx=25, pady=25, highlightbackground=C_BORDER, highlightthickness=1)
    form.pack(fill=X, pady=(0, 20))
    
    Label(form, text="Asignar Calificación a Materia", font=(FONT_FAMILY, 14, "bold"), fg=C_SIDEBAR, bg=C_CARD).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0,20))

    # Obtener catálogos
    estudiantes_db = ejecutar_query("SELECT numero_de_cuenta, nombre FROM estudiante")
    lista_estudiantes = [f"{e[0]} - {e[1]}" for e in estudiantes_db] if estudiantes_db else []
    
    materias_db = ejecutar_query("SELECT clave_materia, asignatura FROM materia")
    lista_materias = [f"{m[0]} - {m[1]}" for m in materias_db] if materias_db else []

    Label(form, text="Estudiante", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=0, sticky="w", pady=(0,5), padx=(0,15))
    cb_estudiante = ttk.Combobox(form, values=lista_estudiantes, state="readonly", font=(FONT_FAMILY, 11))
    cb_estudiante.grid(row=2, column=0, sticky="ew", padx=(0, 15), ipady=5)
    
    Label(form, text="Materia a calificar/inscribir", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=1, sticky="w", pady=(0,5), padx=(0,15))
    cb_materia = ttk.Combobox(form, values=lista_materias, state="readonly", font=(FONT_FAMILY, 11))
    cb_materia.grid(row=2, column=1, sticky="ew", padx=(0, 15), ipady=5)
    
    Label(form, text="Calificación (0-10)", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=2, sticky="w", pady=(0,5))
    ent_calif = Entry(form, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_calif.grid(row=2, column=2, sticky="ew", ipady=6)

    form.grid_columnconfigure(0, weight=1)
    form.grid_columnconfigure(1, weight=1)

    # Tabla de historial del alumno seleccionado
    tabla_frame = Frame(body, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
    tabla_frame.pack(expand=True, fill=BOTH)
    
    tree = ttk.Treeview(tabla_frame, columns=("Clave", "Materia", "Calificacion"), show="headings", style="Treeview")
    tree.heading("Clave", text="Clave Materia")
    tree.heading("Materia", text="Asignatura")
    tree.heading("Calificacion", text="Calificación")
    
    tree.column("Clave", width=100, anchor="center")
    tree.column("Materia", width=400, anchor="w")
    tree.column("Calificacion", width=100, anchor="center")
    
    tree.pack(side=LEFT, expand=True, fill=BOTH)
    
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    def actualizar_tabla(event=None):
        for item in tree.get_children():
            tree.delete(item)
            
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
            for row in historial:
                tree.insert("", END, values=row)

    cb_estudiante.bind("<<ComboboxSelected>>", actualizar_tabla)

    def guardar_calificacion():
        sel_est = cb_estudiante.get()
        sel_mat = cb_materia.get()
        calif = ent_calif.get()
        
        if sel_est and sel_mat and calif:
            try:
                calif_float = float(calif)
                if calif_float < 0 or calif_float > 10:
                    raise ValueError
            except:
                messagebox.showwarning("Error", "La calificación debe ser un número entre 0 y 10.")
                return
                
            cuenta = sel_est.split(" - ")[0]
            clave = sel_mat.split(" - ")[0]
            
            # Inserta o actualiza la calificación de esa materia
            ejecutar_query("INSERT OR REPLACE INTO calificaciones (numero_de_cuenta, clave_materia, calificacion) VALUES (?, ?, ?)", (cuenta, clave, calif_float))
            
            # Recalcular promedio general
            actualizar_promedio(cuenta)
            
            # También lo inscribimos al grupo si no estaba para que se refleje (opcional pero bueno para la lógica)
            # Primero averiguamos el grupo de la materia
            res_grupo = ejecutar_query("SELECT grupo FROM materia WHERE clave_materia = ?", (clave,))
            if res_grupo:
                ejecutar_query("INSERT OR IGNORE INTO estudiante_grupo (numero_de_cuenta, grupo) VALUES (?, ?)", (cuenta, res_grupo[0][0]))
            
            messagebox.showinfo("Éxito", "Calificación registrada y promedio actualizado.")
            ent_calif.delete(0, END)
            actualizar_tabla()
        else:
            messagebox.showwarning("Error", "Completa todos los campos.")

    btn_guardar = Button(form, text="Registrar Calificación", font=(FONT_FAMILY, 10, "bold"), command=guardar_calificacion, bg=C_SIDEBAR, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_guardar.grid(row=3, column=0, columnspan=3, sticky="e", pady=(20, 0), ipadx=20, ipady=8)


# =========================
# DATOS DE USUARIO
# =========================
usuario_cuenta = sys.argv[1] if len(sys.argv) > 1 else "admin123"
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

btn_calif = Button(sidebar, text="📝 Calificaciones", font=(FONT_FAMILY, 10), fg=C_WHITE, bg=C_SIDEBAR, bd=0, anchor="w", padx=18, cursor="hand2")
btn_calif.pack(fill=X, ipady=12)
btn_calif.config(command=lambda: abrir_seccion("Calificaciones", btn_calif, vista_calificaciones))
btn_calif.bind("<Enter>", lambda e: on_sb_enter(e, btn_calif))
btn_calif.bind("<Leave>", lambda e: on_sb_leave(e, btn_calif))


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
