from tkinter import *
import tkinter as tk
from tkinter import ttk
import os
import sys
import subprocess
import threading
import sqlite3
from tkinter import messagebox
import random
import unicodedata
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter

try:
    import speech_recognition as sr
except ImportError:
    sr = None

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

    Frame(area_contenido, bg=C_BORDER, height=1).pack(fill=X)

    # Contenedor dinámico
    ph = Frame(area_contenido, bg=C_BG, padx=30, pady=20)
    ph.pack(expand=True, fill=BOTH)

    # --- LÓGICA DE BASE DE DATOS ---
    try:
        conn = sqlite3.connect('control_escolar.db')
        cursor = conn.cursor()

        if seccion == "Inicio":
            cursor.execute("SELECT carrera, promedio_general FROM estudiante WHERE numero_de_cuenta = ?", (usuario_cuenta,))
            resultado = cursor.fetchone()
            
            carrera = resultado[0] if resultado and resultado[0] else "No asignada"
            promedio = resultado[1] if resultado and resultado[1] else 0.0
            
            # Tarjeta de Info Estudiante
            card = Frame(ph, bg=C_CARD, padx=20, pady=20, highlightbackground=C_BORDER, highlightthickness=1)
            card.pack(fill=X, pady=10)
            
            Label(card, text=f"Bienvenido, {usuario_nombre}", font=(FONT_FAMILY, 16, "bold"), bg=C_CARD, fg=C_SIDEBAR).pack(anchor="w")
            Label(card, text=f"Número de Cuenta: {usuario_cuenta}", font=(FONT_FAMILY, 12), bg=C_CARD, fg=C_TEXT).pack(anchor="w", pady=(10, 0))
            Label(card, text=f"Carrera: {carrera}", font=(FONT_FAMILY, 12), bg=C_CARD, fg=C_TEXT).pack(anchor="w", pady=2)
            Label(card, text=f"Promedio General: {promedio}", font=(FONT_FAMILY, 14, "bold"), bg=C_CARD, fg="#2E8B45").pack(anchor="w", pady=(10, 0))

        elif seccion == "Trayectoria":
            Label(ph, text="Materias Cursadas y Calificaciones", font=(FONT_FAMILY, 14, "bold"), bg=C_BG, fg=C_TEXT).pack(anchor="w", pady=(0, 10))
            
            # Estilos de tabla
            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview.Heading", font=(FONT_FAMILY, 10, "bold"), background=C_SIDEBAR, foreground=C_WHITE)
            style.configure("Treeview", font=(FONT_FAMILY, 11), rowheight=30)
            
            # Crear tabla (Treeview)
            columnas = ("clave", "asignatura", "calificacion")
            tabla = ttk.Treeview(ph, columns=columnas, show="headings", height=10)
            tabla.heading("clave", text="Clave")
            tabla.heading("asignatura", text="Asignatura")
            tabla.heading("calificacion", text="Calificación")
            
            tabla.column("clave", width=100, anchor=CENTER)
            tabla.column("asignatura", width=300, anchor=W)
            tabla.column("calificacion", width=100, anchor=CENTER)
            
            cursor.execute('''
                SELECT m.clave_materia, m.asignatura, c.calificacion, m.grupo 
                FROM calificaciones c 
                JOIN materia m ON c.clave_materia = m.clave_materia 
                WHERE c.numero_de_cuenta = ?
            ''', (usuario_cuenta,))
            materias = cursor.fetchall()
            
            for m in materias:
                tabla.insert("", "end", values=(m[0], m[1], m[2]))
                
            tabla.pack(fill=BOTH, expand=True)

            def generar_tira_pdf():
                pdf_filename = os.path.join("PDF'S", f"Tira_Materias_{usuario_cuenta}.pdf")
                try:
                    c = canvas.Canvas(pdf_filename, pagesize=letter)
                    
                    # Colores institucionales
                    verde_uaem = (26/255.0, 92/255.0, 40/255.0)
                    
                    # Logo (si existe)
                    try:
                        c.drawImage("Media/Logo_de_la_UAEMex.png", 50, 695, width=80, height=60, mask='auto')
                    except Exception:
                        pass
                        
                    # Encabezados
                    c.setFillColorRGB(*verde_uaem)
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(140, 740, "Universidad Autónoma del Estado de México")
                    
                    c.setFillColorRGB(0, 0, 0)
                    c.setFont("Helvetica", 9)
                    c.drawString(140, 725, "Secretaría de Docencia")
                    c.drawString(140, 713, "Dirección de Control Escolar")
                    
                    # Títulos Centrados
                    c.setFont("Helvetica", 11)
                    c.drawCentredString(306, 675, "PERIODO DE CURSOS 2026")
                    c.setFont("Helvetica-Bold", 12)
                    c.drawCentredString(306, 655, "HOJA DE INSCRIPCIÓN POR PLAN")
                    
                    # Caja de Datos del Alumno
                    c.setLineWidth(1)
                    c.setStrokeColorRGB(*verde_uaem)
                    c.rect(50, 585, 512, 50)
                    
                    c.setFillColorRGB(0, 0, 0)
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(55, 620, f"CUENTA:")
                    c.setFont("Helvetica", 10)
                    c.drawString(110, 620, f"{usuario_cuenta}")
                    
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(55, 600, f"NOMBRE:")
                    c.setFont("Helvetica", 10)
                    c.drawString(110, 600, f"{usuario_nombre}")
                    
                    # Encabezado de Tabla
                    y = 560
                    c.setFillColorRGB(*verde_uaem)
                    c.rect(50, y-5, 512, 20, fill=1)
                    
                    c.setFillColorRGB(1, 1, 1) # Texto blanco
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(55, y, "CLAVE MATERIA")
                    c.drawString(180, y, "MATERIA")
                    c.drawString(450, y, "GRUPO")
                    c.drawString(510, y, "CALIF.")
                    
                    c.setFillColorRGB(0, 0, 0)
                    c.setFont("Helvetica", 9)
                    y -= 25
                    
                    y_start_table = 575
                    
                    for i, m in enumerate(materias):
                        if i % 2 == 0:
                            c.setFillColorRGB(0.96, 0.98, 0.96)
                            c.rect(50, y-5, 512, 20, fill=1, stroke=0)
                            c.setFillColorRGB(0, 0, 0)
                            
                        c.drawString(55, y, str(m[0]))
                        
                        asig = str(m[1])
                        if len(asig) > 50: asig = asig[:47] + "..."
                        c.drawString(180, y, asig)
                        
                        grupo_val = str(m[3]) if m[3] else "N/A"
                        c.drawString(450, y, grupo_val)
                        
                        calif_val = str(m[2]) if m[2] is not None else "S/C"
                        c.drawString(510, y, calif_val)
                        
                        y -= 20
                        if y < 100:
                            c.setLineWidth(0.5)
                            c.setStrokeColorRGB(*verde_uaem)
                            c.rect(50, y+15, 512, y_start_table - (y+15))
                            
                            c.showPage()
                            y = 750
                            y_start_table = y + 15
                            c.setFont("Helvetica", 9)
                            c.setFillColorRGB(0, 0, 0)
                    
                    c.setLineWidth(0.5)
                    c.setStrokeColorRGB(*verde_uaem)
                    c.rect(50, y+15, 512, y_start_table - (y+15))
                    
                    # Footer con código de barras
                    c.setFillColorRGB(0, 0, 0)
                    barcode = code128.Code128(usuario_cuenta, barHeight=30, barWidth=1.2)
                    barcode.drawOn(c, 50, y - 30)
                    
                    c.setFont("Helvetica-Oblique", 8)
                    c.drawString(50, y - 45, "Documento de carácter informativo. Consérvelo para aclaraciones posteriores.")
                    
                    c.save()
                    messagebox.showinfo("Éxito", f"Tira de materias descargada con formato UAEMex:\n{pdf_filename}")
                except Exception as ex:
                    messagebox.showerror("Error", f"No se pudo generar el PDF: {ex}")

            btn_descarga = Button(ph, text="📄 Descargar Tira de Materias (PDF)", font=(FONT_FAMILY, 10, "bold"), command=generar_tira_pdf, bg=C_SIDEBAR, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
            btn_descarga.pack(pady=(15, 0), ipadx=20, ipady=8, anchor="w")

        elif seccion == "Inscripción y Reinscripción":
            Label(ph, text="Grupos Inscritos", font=(FONT_FAMILY, 14, "bold"), bg=C_BG, fg=C_TEXT).pack(anchor="w", pady=(0, 10))
            
            cursor.execute('''
                SELECT grupo FROM estudiante_grupo WHERE numero_de_cuenta = ?
            ''', (usuario_cuenta,))
            grupos = cursor.fetchall()
            
            if not grupos:
                Label(ph, text="No estás inscrito en ningún grupo actualmente.", font=(FONT_FAMILY, 12), bg=C_BG, fg=C_MUTED).pack(anchor="w")
            else:
                for g in grupos:
                    lbl_grupo = Label(ph, text=f"📚 Grupo: {g[0]}", font=(FONT_FAMILY, 12), bg=C_CARD, fg=C_SIDEBAR, padx=15, pady=10, highlightbackground=C_BORDER, highlightthickness=1)
                    lbl_grupo.pack(fill=X, pady=5)
        elif seccion == "Pagos":
            Label(ph, text="Generación de Referencia de Pago", font=(FONT_FAMILY, 14, "bold"), bg=C_BG, fg=C_TEXT).pack(anchor="w", pady=(0, 10))
            
            # Generar referencia de pago aleatoria basada en la cuenta (20 dígitos)
            random.seed(usuario_cuenta + "pago")
            ref_num = f"{usuario_cuenta}{random.randint(1000000000000, 9999999999999)}"
            
            card = Frame(ph, bg=C_CARD, padx=20, pady=20, highlightbackground=C_BORDER, highlightthickness=1)
            card.pack(fill=X, pady=10)
            
            Label(card, text="Tu Referencia de Pago es:", font=(FONT_FAMILY, 12), bg=C_CARD, fg=C_MUTED).pack(anchor="center")
            Label(card, text=ref_num, font=(FONT_FAMILY, 20, "bold"), bg=C_CARD, fg=C_SIDEBAR).pack(anchor="center", pady=10)
            
            def generar_pdf():
                pdf_filename = os.path.join("PDF'S", f"Referencia_Pago_{usuario_cuenta}.pdf")
                try:
                    c = canvas.Canvas(pdf_filename, pagesize=letter)
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(100, 750, "Referencia de Pago Universitaria")
                    
                    c.setFont("Helvetica", 12)
                    c.drawString(100, 720, f"Estudiante: {usuario_nombre}")
                    c.drawString(100, 700, f"No. de Cuenta: {usuario_cuenta}")
                    c.drawString(100, 680, f"Concepto: Pago de Colegiatura/Servicios")
                    c.drawString(100, 640, f"Referencia: {ref_num}")
                    
                    # Dibujar código de barras
                    barcode = code128.Code128(ref_num, barHeight=50, barWidth=1.5)
                    barcode.drawOn(c, 100, 560)
                    
                    c.setFont("Helvetica-Oblique", 10)
                    c.drawString(100, 530, "Por favor, presente este documento en ventanilla bancaria.")
                    
                    c.save()
                    messagebox.showinfo("Éxito", f"El PDF de la referencia de pago se ha guardado como:\n{pdf_filename}")
                except Exception as ex:
                    messagebox.showerror("Error", f"No se pudo generar el PDF: {ex}")
            
            btn_pdf = Button(card, text="📄 Descargar PDF con Código de Barras", font=(FONT_FAMILY, 10, "bold"), command=generar_pdf, bg=C_SIDEBAR, fg=C_WHITE, activebackground="#2E8B45", activeforeground=C_WHITE, bd=0, cursor="hand2")
            btn_pdf.pack(pady=(15, 0), ipadx=20, ipady=8)

        elif seccion == "Servicio Social":
            Label(ph, text="Trámites de Servicio Social", font=(FONT_FAMILY, 14, "bold"), bg=C_BG, fg=C_TEXT).pack(anchor="w", pady=(0, 10))
            
            card = Frame(ph, bg=C_CARD, padx=20, pady=20, highlightbackground=C_BORDER, highlightthickness=1)
            card.pack(fill=X, pady=10)
            
            Label(card, text="Requisitos para liberar el Servicio Social:", font=(FONT_FAMILY, 12, "bold"), bg=C_CARD, fg=C_SIDEBAR).pack(anchor="w")
            requisitos = [
                "1. Contar con el 70% de créditos aprobados.",
                "2. Asistir a la plática de inducción.",
                "3. Presentar carta de aceptación de la dependencia.",
                "4. Cubrir un total de 480 horas en un periodo no menor a 6 meses."
            ]
            for req in requisitos:
                Label(card, text=req, font=(FONT_FAMILY, 11), bg=C_CARD, fg=C_TEXT).pack(anchor="w", pady=2)
                
            Label(card, text="Para más información, acércate a la coordinación de extensión y vinculación.", font=(FONT_FAMILY, 10, "italic"), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(15,0))

        elif seccion == "Herramientas":
            Label(ph, text="Herramientas y Credenciales", font=(FONT_FAMILY, 14, "bold"), bg=C_BG, fg=C_TEXT).pack(anchor="w", pady=(0, 10))
            
            card = Frame(ph, bg=C_CARD, padx=20, pady=20, highlightbackground=C_BORDER, highlightthickness=1)
            card.pack(fill=X, pady=10)
            
            # Obtener contraseña
            cursor.execute("SELECT contraseña FROM estudiante WHERE numero_de_cuenta = ?", (usuario_cuenta,))
            res_pass = cursor.fetchone()
            user_pass = res_pass[0] if res_pass else "N/A"
            
            # Generar correo único determinista
            def remover_acentos(txt):
                return ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')
                
            nombre_limpio = remover_acentos(usuario_nombre.lower()).split()
            primer_nombre = nombre_limpio[0] if len(nombre_limpio) > 0 else "user"
            apellido_p = nombre_limpio[1] if len(nombre_limpio) > 1 else "ap"
            letra_apellido_m = nombre_limpio[2][0] if len(nombre_limpio) > 2 else "m"
            
            random.seed(usuario_cuenta + "correo")
            tres_digitos = f"{random.randint(100, 999)}"
            
            correo = f"{primer_nombre}{apellido_p}{letra_apellido_m}{tres_digitos}@uaemex.mx"
            
            Label(card, text="Credenciales Institucionales", font=(FONT_FAMILY, 12, "bold"), bg=C_CARD, fg=C_SIDEBAR).pack(anchor="w", pady=(0, 10))
            
            Label(card, text=f"Usuario (No. de Cuenta): {usuario_cuenta}", font=(FONT_FAMILY, 11), bg=C_CARD, fg=C_TEXT).pack(anchor="w", pady=2)
            Label(card, text=f"Contraseña de Acceso: {user_pass}", font=(FONT_FAMILY, 11), bg=C_CARD, fg=C_TEXT).pack(anchor="w", pady=2)
            Label(card, text=f"Correo Electrónico Institucional: {correo}", font=(FONT_FAMILY, 11, "bold"), bg=C_CARD, fg="#2E8B45").pack(anchor="w", pady=(10, 2))
            
            Label(card, text="Usa este correo para acceder a Office 365, Teams y biblioteca virtual.", font=(FONT_FAMILY, 10, "italic"), bg=C_CARD, fg=C_MUTED).pack(anchor="w", pady=(10,0))

        elif seccion == "Directorio":
            Label(ph, text="Directorio Institucional", font=(FONT_FAMILY, 14, "bold"), bg=C_BG, fg=C_TEXT).pack(anchor="w", pady=(0, 10))
            
            contactos = [
                ("Control Escolar (Administración Central)", "dcontrole@uaemex.mx", "(722) 226 23 45"),
                ("Clínica Multidisciplinaria de Salud", "cms@uaemex.mx", "(722) 212 80 27 / Ext. 118"),
                ("Rectoría UAEMex", "rectoria@uaemex.mx", "(722) 226 23 00"),
                ("Soporte Técnico Institucional (DTIC)", "dtic@uaemex.mx", "(722) 226 23 00")
            ]
            
            for depto, correo_dep, ext in contactos:
                c_card = Frame(ph, bg=C_CARD, padx=15, pady=10, highlightbackground=C_BORDER, highlightthickness=1)
                c_card.pack(fill=X, pady=5)
                Label(c_card, text=depto, font=(FONT_FAMILY, 11, "bold"), bg=C_CARD, fg=C_SIDEBAR).pack(anchor="w")
                Label(c_card, text=f"✉️ {correo_dep}   |   📞 {ext}", font=(FONT_FAMILY, 10), bg=C_CARD, fg=C_TEXT).pack(anchor="w")

        else:
            # Placeholder genérico
            Label(ph, text=f"📋  {seccion}", font=(FONT_FAMILY, 15), fg=C_MUTED, bg=C_BG).place(relx=0.5, rely=0.45, anchor="center")
            
        conn.close()
    except sqlite3.Error as e:
        Label(ph, text=f"Error de base de datos: {e}", fg="red", bg=C_BG).pack()


# =========================
# FUNCIONES DE VOZ
# =========================
def ejecutar_comando_voz(comando):
    print(comando)
    comando = comando.lower()

    

    if "inicio" in comando:
        abrir_seccion("Inicio", botones_sidebar[0])
    elif "trayectoria" in comando:
        abrir_seccion("Trayectoria", botones_sidebar[1])
    elif "inscripción" in comando or "reinscripción" in comando:
        abrir_seccion("Inscripción y Reinscripción", botones_sidebar[2])
    elif "pagos" in comando or "pago" in comando:
        abrir_seccion("Pagos", botones_sidebar[3])
    elif "servicio" in comando:
        abrir_seccion("Servicio Social", botones_sidebar[4])
    elif "herramienta" in comando:
        abrir_seccion("Herramientas", botones_sidebar[5])
    elif "directorio" in comando:
        abrir_seccion("Directorio", botones_sidebar[6])
    else:
        messagebox.showinfo("Comando no reconocido", f"No entendí la sección a partir de: '{comando}'")

def hilo_escuchar():
    if sr is None:
        ventana.after(0, lambda: messagebox.showerror("Error", "La librería speech_recognition no está instalada.\nInstálala con: pip install SpeechRecognition pyaudio"))
        return

    recognizer = sr.Recognizer()
    try:
        # Actualizar UI para mostrar que está escuchando
        ventana.after(0, lambda: btn_mic.config(text="  Escuchando...", bg="#2E8B45"))
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
        comando = recognizer.recognize_google(audio, language="es-ES")
        # Ejecutar en el hilo principal de Tkinter
        ventana.after(0, ejecutar_comando_voz, comando)
        
    except sr.UnknownValueError:
        print("No se entendió el audio (UnknownValueError)")
        ventana.after(0, lambda: messagebox.showwarning("Micrófono", "No pude entender lo que dijiste."))
    except sr.RequestError as e:
        print(f"Error de conexión con Google: {e}")
        ventana.after(0, lambda: messagebox.showerror("Error de Servicio", f"No se pudo conectar a Google Speech: {e}"))
    except Exception as e:
        print(f"Error inesperado al escuchar: {type(e).__name__} - {e}")
    finally:
        # Restaurar botón
        ventana.after(0, lambda: btn_mic.config(text="  Usar Micrófono", bg=C_SIDEBAR))

def iniciar_escucha():
    threading.Thread(target=hilo_escuchar, daemon=True).start()


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
        cursor="hand2",
        command=iniciar_escucha
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
        cursor="hand2",
        command=iniciar_escucha
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
    text="Universidad Autónoma del Estado de México  •  Sistema de Control Escolar  •  © 2026",
    font=(FONT_FAMILY, 9),
    fg=C_MUTED,
    bg=C_TOPBAR
).pack(pady=7)

# =========================
# MAIN LOOP
# =========================
ventana.mainloop()