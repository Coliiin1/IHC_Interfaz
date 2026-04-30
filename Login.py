from tkinter import *
import tkinter as tk

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
# FUNCIONES PRINCIPALES
# =========================

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


# =========================
# VENTANA PRINCIPAL
# =========================

ventana = Tk()
ventana.title("Sistema Universitario")
ventana.geometry("650x720")
ventana.resizable(False, False)

# Paleta institucional
COLOR_FONDO = "#f3e8d3"
COLOR_PRINCIPAL = "#195021"
COLOR_SECUNDARIO = "#2f6b3c"
COLOR_INPUT = "#f8f3ea"
COLOR_TEXTO = "#195021"

ventana.config(bg=COLOR_FONDO)

# =========================
# VARIABLES
# =========================

# Cambia el nombre por tu logo
ruta_logo = "logo.png"

# =========================
# VALIDACIONES
# =========================

vcmd = (ventana.register(validacion_entrada), '%P')
vcmd2 = (ventana.register(validacion_contraseña), '%P')

# =========================
# CONTENEDOR PRINCIPAL
# =========================

frame_principal = Frame(
    ventana,
    bg="white",
    width=520,
    height=620,
    highlightbackground="#d4c2a3",
    highlightthickness=1
)

frame_principal.place(relx=0.5, rely=0.5, anchor="center")

# =========================
# LOGO
# =========================

try:
    logo = PhotoImage(file="media/Logo_de_la_UAEMex.png")

    logo_label = Label(
        frame_principal,
        image=logo,
        bg="#ffffff"
    )

    logo_label.place(x=180, y=25, width=160, height=148)

except:
    # Espacio reservado para logo
    logo_placeholder = Frame(
        frame_principal,
        bg="#ffffff",
        width=160,
        height=100
    )

    logo_placeholder.place(x=180, y=25)

    texto_logo = Label(
        logo_placeholder,
        text="LOGO\nUNIVERSIDAD",
        font=("Arial", 13, "bold"),
        fg=COLOR_PRINCIPAL,
        bg="#e7dcc8"
    )

    texto_logo.place(relx=0.5, rely=0.5, anchor="center")

# =========================
# TITULOS
# =========================

titulo = Label(
    frame_principal,
    text="Iniciar Sesión",
    font=("Segoe UI", 28, "bold"),
    fg=COLOR_PRINCIPAL,
    bg="white"
)

titulo.place(x=140, y=155)

subtitulo = Label(
    frame_principal,
    text="Sistema de Control Escolar",
    font=("Segoe UI", 12),
    fg=COLOR_SECUNDARIO,
    bg="white"
)

subtitulo.place(x=145, y=205)

# =========================
# USUARIO
# =========================

usuario = Label(
    frame_principal,
    text="No de Cuenta",
    font=("Segoe UI", 12, "bold"),
    fg=COLOR_TEXTO,
    bg="white"
)

usuario.place(x=60, y=280)

usuario_entrada = Entry(
    frame_principal,
    font=("Segoe UI", 14),
    width=35,
    bd=0,
    bg=COLOR_INPUT,
    relief="flat",
    validate="key",
    validatecommand=vcmd
)

usuario_entrada.place(x=60, y=315, height=45)

# Línea decorativa
Frame(
    frame_principal,
    bg=COLOR_PRINCIPAL,
    width=400,
    height=2
).place(x=60, y=360)

# =========================
# CONTRASEÑA
# =========================

contraseña = Label(
    frame_principal,
    text="Contraseña",
    font=("Segoe UI", 12, "bold"),
    fg=COLOR_TEXTO,
    bg="white"
)

contraseña.place(x=60, y=395)

contraseña_entrada = Entry(
    frame_principal,
    font=("Segoe UI", 14),
    width=28,
    bd=0,
    bg=COLOR_INPUT,
    relief="flat",
    show="*",
    validate="key",
    validatecommand=vcmd2
)

contraseña_entrada.place(x=60, y=430, height=45)

Frame(
    frame_principal,
    bg=COLOR_PRINCIPAL,
    width=400,
    height=2
).place(x=60, y=475)

# =========================
# BOTÓN MOSTRAR
# =========================

boton_mostrar = Button(
    frame_principal,
    text="Mostrar",
    command=mostrar_ocultar,
    font=("Segoe UI", 10, "bold"),
    fg=COLOR_FONDO,
    bg=COLOR_PRINCIPAL,
    activebackground=COLOR_SECUNDARIO,
    activeforeground="white",
    bd=0,
    cursor="hand2"
)

boton_mostrar.place(x=380, y=430, width=80, height=45)

# =========================
# BOTÓN LIMPIAR
# =========================

# =========================
# BOTÓN INGRESAR
# =========================

registrar = Button(
    frame_principal,
    text="INGRESAR",
    font=("Segoe UI", 13, "bold"),
    fg=COLOR_FONDO,
    bg=COLOR_PRINCIPAL,
    activebackground=COLOR_SECUNDARIO,
    activeforeground="white",
    bd=0,
    cursor="hand2"
)

registrar.place(x=60, y=525, width=400, height=50)

# =========================
# FOOTER
# =========================

footer = Label(
    ventana,
    text="Universidad Autonoma del Estado de Mexico • Plataforma de Control Escolar",
    font=("Segoe UI", 10),
    fg=COLOR_PRINCIPAL,
    bg=COLOR_FONDO
)

footer.place(relx=0.5, y=690, anchor="center")

# =========================
# MAIN LOOP
# =========================

ventana.mainloop()
