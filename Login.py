from tkinter import *
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import sqlite3

# =========================
# PALETA DE COLORES (Sistema de diseño UAEMex).
# =========================
C_BG        = "#F0F2F5"   # Fondo general gris muy claro
C_CARD      = "#FFFFFF"   # Tarjeta blanca
C_PRIMARY   = "#1A5C28"   # Verde institucional oscuro
C_ACCENT    = "#2E8B45"   # Verde medio (hover / acento)
C_MUTED     = "#6B7280"   # Texto secundario gris
C_BORDER    = "#E5E7EB"   # Borde sutil
C_INPUT_BG  = "#F9FAFB"   # Fondo de campos
C_TEXT      = "#111827"   # Texto principal casi negro
C_WHITE     = "#FFFFFF"
C_ERROR     = "#DC2626"

FONT_FAMILY = "Segoe UI"

# =========================
# FUNCIONES DE VALIDACIÓN
# =========================

def validacion_entrada(content):
    if content == "":
        return True
    return content.isdigit() and len(content) <= 7


def validacion_contraseña(content):
    if content == "":
        return True
    return content.isalnum() and len(content) <= 11


# =========================
# ESTADO GLOBAL
# =========================
es_admin = False

# =========================
# FUNCIONES PRINCIPALES
# =========================

def toggle_modo():
    global es_admin
    es_admin = not es_admin
    if es_admin:
        lbl_titulo.config(text="Iniciar Sesión")
        lbl_subtitulo.config(text="Portal Administrativo", fg="#1A5C28", font=(FONT_FAMILY, 12, "bold"))
        btn_toggle.config(text="← Volver al Portal de Estudiantes")
    else:
        lbl_titulo.config(text="Iniciar Sesión")
        lbl_subtitulo.config(text="Portal Estudiantil", fg=C_MUTED, font=(FONT_FAMILY, 11))
        btn_toggle.config(text="Acceso Administrativo →")


def mostrar_ocultar():
    if contraseña_entrada.cget("show") == "*":
        contraseña_entrada.config(show="")
        boton_mostrar.config(text="Ocultar")
    else:
        contraseña_entrada.config(show="*")
        boton_mostrar.config(text="Mostrar")


def limpiar_campos():
    usuario_entrada.delete(0, END)
    contraseña_entrada.delete(0, END)


def login():
    """Valida credenciales en la DB y abre la ventana correspondiente al rol."""
    cuenta = usuario_entrada.get().strip()
    clave   = contraseña_entrada.get().strip()

    if not cuenta or not clave:
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    try:
        conn = sqlite3.connect('control_escolar.db')
        cursor = conn.cursor()
        
        # Consultar usuario, password y rol
        cursor.execute('SELECT password, rol, nombre FROM usuarios WHERE num_cuenta = ?', (cuenta,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado and resultado[0] == clave:
            password_db, rol, nombre = resultado
            
            # Validar que el rol coincida con el modo de la interfaz
            if es_admin and rol != 'Admin':
                messagebox.showerror("Acceso Denegado", "Esta cuenta no tiene privilegios de administrador.\nPor favor usa el portal de estudiantes.")
                return
            if not es_admin and rol == 'Admin':
                messagebox.showerror("Acceso Denegado", "Estás intentando entrar como administrador desde el portal de estudiantes.\nUsa el acceso administrativo.")
                return

            ventana.destroy()
            
            # Definir qué script abrir según el rol
            if rol == 'Admin':
                script = "AdminPrincipal.py"
            else:
                script = "MenPrincipal.py"
                
            path_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), script)
            subprocess.Popen([sys.executable, path_script, cuenta, nombre])
        else:
            messagebox.showerror("Error", "Número de cuenta o contraseña incorrectos.")
            contraseña_entrada.delete(0, END)

    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudo conectar: {e}")


# ---- hover helpers ----
def on_enter_btn(e, widget, color):
    widget.config(bg=color)

def on_leave_btn(e, widget, color):
    widget.config(bg=color)


# =========================
# VENTANA PRINCIPAL
# =========================

ventana = Tk()
ventana.title("Sistema de Control Escolar — UAEMex")
ventana.geometry("700x800")
ventana.resizable(False, False)
ventana.config(bg=C_BG)

vcmd  = (ventana.register(validacion_entrada),    '%P')
vcmd2 = (ventana.register(validacion_contraseña), '%P')

# =========================
# FRANJA LATERAL IZQUIERDA (decorativa)
# =========================
franja = Frame(ventana, bg=C_PRIMARY, width=12)
franja.pack(side=LEFT, fill=Y)

# =========================
# CONTENEDOR PRINCIPAL CENTRADO
# =========================
wrapper = Frame(ventana, bg=C_BG)
wrapper.pack(expand=True, fill=BOTH)

card = Frame(
    wrapper,
    bg=C_CARD,
    width=480,
    height=720,
    highlightbackground=C_BORDER,
    highlightthickness=1
)
card.place(relx=0.5, rely=0.5, anchor="center")
card.pack_propagate(False)

# ---- Padding interior ----
inner = Frame(card, bg=C_CARD, padx=50, pady=30)
inner.pack(expand=True, fill=BOTH)

# =========================
# LOGO
# =========================
try:
    logo_img = PhotoImage(file="Media/Logo_de_la_UAEMex.png")
    # Escalar si es demasiado grande (funciona solo con subsample en PNG)
    logo_label = Label(inner, image=logo_img, bg=C_CARD)
    logo_label.image = logo_img
    logo_label.pack(pady=(10, 0))
except Exception:
    ph = Frame(inner, bg=C_BORDER, width=120, height=80)
    ph.pack(pady=(10, 0))
    ph.pack_propagate(False)
    Label(ph, text="UAEMex", font=(FONT_FAMILY, 14, "bold"),
          fg=C_PRIMARY, bg=C_BORDER).place(relx=0.5, rely=0.5, anchor="center")

# =========================
# ENCABEZADO
# =========================
lbl_titulo = Label(
    inner,
    text="Iniciar Sesión",
    font=(FONT_FAMILY, 26, "bold"),
    fg=C_TEXT,
    bg=C_CARD
)
lbl_titulo.pack(pady=(18, 2))

lbl_subtitulo = Label(
    inner,
    text="Portal Estudiantil",
    font=(FONT_FAMILY, 11),
    fg=C_MUTED,
    bg=C_CARD
)
lbl_subtitulo.pack(pady=(0, 24))

# Separador
Frame(inner, bg=C_BORDER, height=1).pack(fill=X, pady=(0, 20))

# =========================
# CAMPO: No. de Cuenta
# =========================
Label(
    inner,
    text="Número de Cuenta",
    font=(FONT_FAMILY, 10, "bold"),
    fg=C_MUTED,
    bg=C_CARD,
    anchor="w"
).pack(fill=X)

usuario_frame = Frame(inner, bg=C_INPUT_BG,
                      highlightbackground=C_BORDER, highlightthickness=1)
usuario_frame.pack(fill=X, pady=(4, 16))

usuario_entrada = Entry(
    usuario_frame,
    font=(FONT_FAMILY, 13),
    bd=0,
    bg=C_INPUT_BG,
    fg=C_TEXT,
    insertbackground=C_PRIMARY,
    relief="flat",
    validate="key",
    validatecommand=vcmd
)
usuario_entrada.pack(fill=X, ipady=10, padx=12)

# focus: cambia borde
def on_focus_in_user(e):
    usuario_frame.config(highlightbackground=C_PRIMARY)
def on_focus_out_user(e):
    usuario_frame.config(highlightbackground=C_BORDER)
usuario_entrada.bind("<FocusIn>",  on_focus_in_user)
usuario_entrada.bind("<FocusOut>", on_focus_out_user)

# =========================
# CAMPO: Contraseña
# =========================
Label(
    inner,
    text="Contraseña",
    font=(FONT_FAMILY, 10, "bold"),
    fg=C_MUTED,
    bg=C_CARD,
    anchor="w"
).pack(fill=X)

pass_outer = Frame(inner, bg=C_INPUT_BG,
                   highlightbackground=C_BORDER, highlightthickness=1)
pass_outer.pack(fill=X, pady=(4, 20))

contraseña_entrada = Entry(
    pass_outer,
    font=(FONT_FAMILY, 13),
    bd=0,
    bg=C_INPUT_BG,
    fg=C_TEXT,
    insertbackground=C_PRIMARY,
    relief="flat",
    show="*",
    validate="key",
    validatecommand=vcmd2
)
contraseña_entrada.pack(side=LEFT, fill=X, expand=True, ipady=10, padx=12)

def on_focus_in_pass(e):
    pass_outer.config(highlightbackground=C_PRIMARY)
def on_focus_out_pass(e):
    pass_outer.config(highlightbackground=C_BORDER)
contraseña_entrada.bind("<FocusIn>",  on_focus_in_pass)
contraseña_entrada.bind("<FocusOut>", on_focus_out_pass)

boton_mostrar = Button(
    pass_outer,
    text="Mostrar",
    command=mostrar_ocultar,
    font=(FONT_FAMILY, 9, "bold"),
    fg=C_PRIMARY,
    bg=C_INPUT_BG,
    activebackground=C_INPUT_BG,
    activeforeground=C_ACCENT,
    bd=0,
    cursor="hand2",
    relief="flat"
)
boton_mostrar.pack(side=RIGHT, padx=8)

# =========================
# BOTÓN INGRESAR
# =========================
btn_ingresar = Button(
    inner,
    text="INGRESAR",
    command=login,
    font=(FONT_FAMILY, 12, "bold"),
    fg=C_WHITE,
    bg=C_PRIMARY,
    activebackground=C_ACCENT,
    activeforeground=C_WHITE,
    bd=0,
    cursor="hand2",
    relief="flat"
)
# Permitir Enter como atajo de teclado
ventana.bind("<Return>", lambda e: login())
btn_ingresar.pack(fill=X, ipady=12)

btn_ingresar.bind("<Enter>", lambda e: btn_ingresar.config(bg=C_ACCENT))
btn_ingresar.bind("<Leave>", lambda e: btn_ingresar.config(bg=C_PRIMARY))

# =========================
# BOTÓN LIMPIAR (secundario)
# =========================
btn_limpiar = Button(
    inner,
    text="Limpiar campos",
    command=limpiar_campos,
    font=(FONT_FAMILY, 10),
    fg=C_MUTED,
    bg=C_CARD,
    activebackground=C_BG,
    activeforeground=C_TEXT,
    bd=0,
    cursor="hand2",
    relief="flat"
)
btn_limpiar.pack(pady=(8, 0))
btn_limpiar.bind("<Enter>", lambda e: btn_limpiar.config(fg=C_PRIMARY))
btn_limpiar.bind("<Leave>", lambda e: btn_limpiar.config(fg=C_MUTED))

# =========================
# BOTÓN MODO ADMIN (Toggle)
# =========================
btn_toggle = Button(
    inner,
    text="Acceso Administrativo →",
    command=toggle_modo,
    font=(FONT_FAMILY, 9, "underline"),
    fg=C_MUTED,
    bg=C_CARD,
    activebackground=C_CARD,
    activeforeground=C_PRIMARY,
    bd=0,
    cursor="hand2",
    relief="flat"
)
btn_toggle.pack(pady=(20, 0))

# =========================
# FOOTER
# =========================
footer = Label(
    ventana,
    text="Universidad Autónoma del Estado de México  •  Plataforma de Control Escolar",
    font=(FONT_FAMILY, 9),
    fg=C_MUTED,
    bg=C_BG
)
footer.pack(side=BOTTOM, pady=14)

# =========================
# MAIN LOOP
# =========================
ventana.mainloop()
