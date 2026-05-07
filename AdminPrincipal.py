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
        cursor = conn.cursor()
        cursor.execute(query, parametros)
        conn.commit()
        res = cursor.fetchall()
        conn.close()
        return res
    except Exception as e:
        messagebox.showerror("Error DB", str(e))
        return None

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
    
    usuarios = ejecutar_query("SELECT COUNT(*) FROM usuarios WHERE rol='Estudiante'")
    count = usuarios[0][0] if usuarios else 0
    
    Label(card, text="🎓 Estudiantes Registrados", font=(FONT_FAMILY, 14, "bold"), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    Label(card, text=str(count), font=(FONT_FAMILY, 48, "bold"), fg=C_PRIMARY, bg=C_CARD).pack(anchor="w", pady=(10, 0))

def vista_gestion_estudiantes():
    header = limpiar_pantalla()
    Label(header, text="Gestión de Estudiantes", font=(FONT_FAMILY, 20, "bold"), fg=C_TEXT, bg=C_CARD).pack(anchor="w")
    Label(header, text="Agrega o modifica los accesos de los alumnos", font=(FONT_FAMILY, 10), fg=C_MUTED, bg=C_CARD).pack(anchor="w")
    
    body = Frame(area_contenido, bg=C_BG, padx=30, pady=30)
    body.pack(expand=True, fill=BOTH)

    # Formulario rápido
    form = Frame(body, bg=C_CARD, padx=25, pady=25, highlightbackground=C_BORDER, highlightthickness=1)
    form.pack(fill=X, pady=(0, 20))
    
    Label(form, text="Agregar / Modificar Estudiante", font=(FONT_FAMILY, 14, "bold"), fg=C_PRIMARY, bg=C_CARD).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0,20))
    
    # Row 1
    Label(form, text="Número de Cuenta", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=0, sticky="w", pady=(0,5), padx=(0,15))
    ent_cuenta = Entry(form, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_cuenta.grid(row=2, column=0, sticky="ew", padx=(0, 15), ipady=6)
    
    Label(form, text="Nombre Completo", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=1, sticky="w", pady=(0,5), padx=(0,15))
    ent_nombre = Entry(form, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_nombre.grid(row=2, column=1, sticky="ew", padx=(0, 15), ipady=6)
    
    Label(form, text="Contraseña", font=(FONT_FAMILY, 10, "bold"), fg=C_MUTED, bg=C_CARD).grid(row=1, column=2, sticky="w", pady=(0,5))
    ent_pass = Entry(form, font=(FONT_FAMILY, 11), bg="#F9FAFB", fg=C_TEXT, relief="solid", bd=1, highlightbackground=C_BORDER)
    ent_pass.grid(row=2, column=2, sticky="ew", ipady=6)

    form.grid_columnconfigure(1, weight=1) # El nombre ocupa más espacio

    def guardar():
        c, n, p = ent_cuenta.get(), ent_nombre.get(), ent_pass.get()
        if c and n and p:
            ejecutar_query("INSERT OR REPLACE INTO usuarios (num_cuenta, nombre, password, rol) VALUES (?, ?, ?, 'Estudiante')", (c, n, p))
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
            vista_gestion_estudiantes()
        else:
            messagebox.showwarning("Error", "Completa todos los campos obligatorios.")

    btn_guardar = Button(form, text="Guardar Cambios", font=(FONT_FAMILY, 10, "bold"), command=guardar, bg=C_PRIMARY, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_guardar.grid(row=3, column=0, columnspan=3, sticky="e", pady=(20, 0), ipadx=20, ipady=8)

    # Estilos de tabla
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=(FONT_FAMILY, 10, "bold"), background="#F9FAFB", foreground=C_MUTED, borderwidth=0)
    style.configure("Treeview", font=(FONT_FAMILY, 10), background=C_CARD, fieldbackground=C_CARD, rowheight=35, borderwidth=0)
    style.map("Treeview", background=[('selected', '#E8F5E9')], foreground=[('selected', C_PRIMARY)])

    # Tabla de estudiantes
    tabla_frame = Frame(body, bg=C_CARD, highlightbackground=C_BORDER, highlightthickness=1)
    tabla_frame.pack(expand=True, fill=BOTH)
    
    tree = ttk.Treeview(tabla_frame, columns=("Cuenta", "Nombre", "Contraseña"), show="headings", style="Treeview")
    tree.heading("Cuenta", text="No. Cuenta")
    tree.heading("Nombre", text="Nombre Completo")
    tree.heading("Contraseña", text="Contraseña")
    
    tree.column("Cuenta", width=150, anchor="center")
    tree.column("Nombre", width=400, anchor="w")
    tree.column("Contraseña", width=200, anchor="center")
    
    tree.pack(side=LEFT, expand=True, fill=BOTH)
    
    # Scrollbar para la tabla
    scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    estudiantes = ejecutar_query("SELECT num_cuenta, nombre, password FROM usuarios WHERE rol='Estudiante'")
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
            ejecutar_query("DELETE FROM usuarios WHERE num_cuenta = ?", (str(cuenta_eliminar),))
            messagebox.showinfo("Éxito", "Alumno dado de baja correctamente.")
            vista_gestion_estudiantes()

    btn_eliminar = Button(body, text="Dar de baja seleccionado", font=(FONT_FAMILY, 10, "bold"), command=eliminar_seleccionado, bg="#DC2626", fg=C_WHITE, activebackground="#B91C1C", activeforeground=C_WHITE, bd=0, cursor="hand2")
    btn_eliminar.pack(anchor="e", pady=(15, 0), ipadx=20, ipady=8)

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

C_PRIMARY = C_SIDEBAR # Alias para compatibilidad con el render anterior

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
