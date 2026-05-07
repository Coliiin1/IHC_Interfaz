from tkinter import *
import tkinter as tk
import os
import sys
import subprocess

# =========================
# SISTEMA DE DISEÑO UAEMex
# =========================
C_BG        = "#F0F2F5"   # Fondo general
C_SIDEBAR   = "#1A5C28"   # Verde institucional oscuro (sidebar)
C_SIDEBAR_H = "#145020"   # Sidebar hover (más oscuro)
C_BTN_ACT   = "#2E8B45"   # Verde activo / seleccionado
C_TOPBAR    = "#FFFFFF"   # Barra superior
C_CARD      = "#FFFFFF"   # Área de contenido
C_TEXT      = "#111827"   # Texto principal
C_MUTED     = "#6B7280"   # Texto secundario
C_BORDER    = "#E5E7EB"   # Borde sutil
C_WHITE     = "#FFFFFF"
C_BTN_TXT   = "#FFFFFF"   # Texto de botones sidebar

FONT_FAMILY = "Segoe UI"

# =========================
# ESTADO GLOBAL
# =========================
btn_activo = None  # Botón actualmente activo en sidebar

# =========================
# FUNCIONES
# =========================
def cerrar():
    """Cierra la sesión y regresa al Login."""
    try:
        # Intentar obtener la ruta absoluta de Login.py
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Login.py")
        subprocess.Popen([sys.executable, script])
    except Exception as e:
        print(f"Error al abrir el login: {e}")
    ventana.destroy()

def inicio():
    mostrar_contenido("Inicio")

def abrir_seccion(nombre, btn):
    """Resalta el botón activo y cambia el área de contenido."""
    global btn_activo
    # Restaurar botón anterior
    if btn_activo and btn_activo != btn:
        btn_activo.config(bg=C_SIDEBAR, fg=C_BTN_TXT,
                          relief="flat", font=(FONT_FAMILY, 10))
    # Activar botón actual
    btn.config(bg=C_BTN_ACT, fg=C_WHITE,
               relief="flat", font=(FONT_FAMILY, 10, "bold"))
    btn_activo = btn
    mostrar_contenido(nombre)


def mostrar_contenido(seccion):
    # Limpiar área de contenido
    for widget in area_contenido.winfo_children():
        widget.destroy()

    # Encabezado de sección
    Frame(area_contenido, bg=C_BORDER, height=1).pack(fill=X)

    header = Frame(area_contenido, bg=C_CARD, pady=20, padx=30)
    header.pack(fill=X)

    Label(
        header,
        text=seccion,
        font=(FONT_FAMILY, 20, "bold"),
        fg=C_TEXT,
        bg=C_CARD
    ).pack(anchor="w")

    Label(
        header,
        text=f"Sección: {seccion}",
        font=(FONT_FAMILY, 10),
        fg=C_MUTED,
        bg=C_CARD
    ).pack(anchor="w")

    Frame(area_contenido, bg=C_BORDER, height=1).pack(fill=X)

    # Placeholder de contenido
    ph = Frame(area_contenido, bg=C_BG)
    ph.pack(expand=True, fill=BOTH)
    Label(
        ph,
        text=f"📋  {seccion}",
        font=(FONT_FAMILY, 15),
        fg=C_MUTED,
        bg=C_BG
    ).place(relx=0.5, rely=0.45, anchor="center")


# ---- Hover helpers para sidebar ----
def on_sb_enter(e, btn):
    if btn != btn_activo:
        btn.config(bg="#22703A")

def on_sb_leave(e, btn):
    if btn != btn_activo:
        btn.config(bg=C_SIDEBAR)


# =========================
# DATOS DE USUARIO
# =========================
usuario_cuenta = sys.argv[1] if len(sys.argv) > 1 else "1234567"
usuario_nombre = sys.argv[2] if len(sys.argv) > 2 else "Juan Pérez Sánchez"

# Generar iniciales
partes = usuario_nombre.split()
iniciales = "".join(p[0] for p in partes[:2]).upper() if partes else "U"

# =========================
# VENTANA PRINCIPAL
# =========================
ventana = Tk()
ventana.geometry("1050x680")
ventana.title("Sistema de Control Escolar — UAEMex")
ventana.resizable(True, True)
ventana.config(bg=C_BG)

try:
    ventana.iconbitmap("ICONO_CASA.ico")
except Exception:
    pass

# =========================
# TOPBAR
# =========================
topbar = Frame(ventana, bg=C_TOPBAR, height=60,
               highlightbackground=C_BORDER, highlightthickness=1)
topbar.pack(side=TOP, fill=X)
topbar.pack_propagate(False)

# Nombre del sistema
Label(
    topbar,
    text="UAEMex  •  Control Escolar",
    font=(FONT_FAMILY, 13, "bold"),
    fg=C_SIDEBAR,
    bg=C_TOPBAR
).pack(side=LEFT, padx=24, pady=14)

# Info del usuario (derecha)
user_frame = Frame(topbar, bg=C_TOPBAR)
user_frame.pack(side=RIGHT, padx=24)

try:
    perfil_img = PhotoImage(file="PERFIL_PNG.png")
    lbl_perfil = Label(user_frame, image=perfil_img, bg=C_TOPBAR)
    lbl_perfil.image = perfil_img
    lbl_perfil.pack(side=LEFT, padx=(0, 8))
except Exception:
    # Círculo de avatar con inicial
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
    text="Estudiante",
    font=(FONT_FAMILY, 9),
    fg=C_MUTED,
    bg=C_TOPBAR
).pack(side=LEFT, padx=(6, 0))

# =========================
# CUERPO (sidebar + contenido)
# =========================
cuerpo = Frame(ventana, bg=C_BG)
cuerpo.pack(expand=True, fill=BOTH)

# =========================
# SIDEBAR
# =========================
sidebar = Frame(cuerpo, bg=C_SIDEBAR, width=200)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)

# Separador visual
Frame(sidebar, bg="#145020", height=1).pack(fill=X)

# Etiqueta de navegación
Label(
    sidebar,
    text="MENÚ",
    font=(FONT_FAMILY, 8, "bold"),
    fg="#6BBF80",
    bg=C_SIDEBAR
).pack(anchor="w", padx=18, pady=(14, 4))

# ---- Definición de secciones ----
secciones = [
    ("🏠  Inicio",                    "Inicio"),
    ("📈  Trayectoria",               "Trayectoria"),
    ("📝  Inscripción y Reinscripción","Inscripción y Reinscripción"),
    ("💳  Pagos",                     "Pagos"),
    ("🤝  Servicio Social",           "Servicio Social"),
    ("🔧  Herramientas",              "Herramientas"),
    ("📒  Directorio",                "Directorio"),
]

botones_sidebar = []

for texto, nombre in secciones:
    btn = Button(
        sidebar,
        text=texto,
        font=(FONT_FAMILY, 10),
        fg=C_BTN_TXT,
        bg=C_SIDEBAR,
        activebackground=C_BTN_ACT,
        activeforeground=C_WHITE,
        bd=0,
        relief="flat",
        anchor="w",
        padx=18,
        cursor="hand2"
    )
    btn.pack(fill=X, ipady=10)
    # Capturar variables en closure
    btn.config(command=lambda n=nombre, b=btn: abrir_seccion(n, b))
    btn.bind("<Enter>", lambda e, b=btn: on_sb_enter(e, b))
    btn.bind("<Leave>", lambda e, b=btn: on_sb_leave(e, b))
    botones_sidebar.append(btn)

# Separador inferior
Frame(sidebar, bg="#145020", height=1).pack(fill=X, pady=(12, 0))

# Botón Usar Micrófono
try:
    mic_img = PhotoImage(file="micro_microphone_4764.png")
    btn_mic = Button(
        sidebar,
        image=mic_img,
        text="  Usar Micrófono",
        compound="left",
        font=(FONT_FAMILY, 10),
        fg=C_BTN_TXT,
        bg=C_SIDEBAR,
        activebackground="#22703A",
        activeforeground=C_WHITE,
        bd=0,
        relief="flat",
        anchor="w",
        padx=18,
        cursor="hand2"
    )
    btn_mic.image = mic_img
except Exception:
    btn_mic = Button(
        sidebar,
        text="🎤  Usar Micrófono",
        font=(FONT_FAMILY, 10),
        fg=C_BTN_TXT,
        bg=C_SIDEBAR,
        activebackground="#22703A",
        activeforeground=C_WHITE,
        bd=0,
        relief="flat",
        anchor="w",
        padx=18,
        cursor="hand2"
    )
btn_mic.pack(fill=X, ipady=10)
btn_mic.bind("<Enter>", lambda e: btn_mic.config(bg="#22703A"))
btn_mic.bind("<Leave>", lambda e: btn_mic.config(bg=C_SIDEBAR))

# Botón Cerrar Sesión (fijado abajo)
Frame(sidebar, bg="#145020", height=1).pack(fill=X, side=BOTTOM, pady=(0, 0))
btn_cerrar = Button(
    sidebar,
    text="⏻  Cerrar Sesión",
    font=(FONT_FAMILY, 10),
    fg="#F87171",
    bg=C_SIDEBAR,
    activebackground="#7F1D1D",
    activeforeground=C_WHITE,
    bd=0,
    relief="flat",
    anchor="w",
    padx=18,
    cursor="hand2",
    command=cerrar
)
btn_cerrar.pack(fill=X, ipady=10, side=BOTTOM)
btn_cerrar.bind("<Enter>", lambda e: btn_cerrar.config(bg="#7F1D1D", fg=C_WHITE))
btn_cerrar.bind("<Leave>", lambda e: btn_cerrar.config(bg=C_SIDEBAR, fg="#F87171"))

# =========================
# ÁREA DE CONTENIDO
# =========================
area_contenido = Frame(cuerpo, bg=C_CARD)
area_contenido.pack(side=RIGHT, expand=True, fill=BOTH)

# Mostrar "Inicio" por defecto
mostrar_contenido("Inicio")
# Resaltar primer botón
botones_sidebar[0].config(bg=C_BTN_ACT, fg=C_WHITE,
                           font=(FONT_FAMILY, 10, "bold"))
btn_activo = botones_sidebar[0]

# =========================
# FOOTER
# =========================
footer = Frame(ventana, bg=C_TOPBAR,
               highlightbackground=C_BORDER, highlightthickness=1)
footer.pack(side=BOTTOM, fill=X)
Label(
    footer,
    text="Universidad Autónoma del Estado de México  •  Sistema de Control Escolar  •  © 2025",
    font=(FONT_FAMILY, 9),
    fg=C_MUTED,
    bg=C_TOPBAR
).pack(pady=7)

# =========================
# MAIN LOOP
# =========================
ventana.mainloop()