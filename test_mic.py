import speech_recognition as sr

def test_mic():
    print("Micrófonos disponibles:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Micrófono con index {index}: {name}")

    recognizer = sr.Recognizer()
    print("\nUsando el micrófono por defecto...")
    try:
        with sr.Microphone() as source:
            print("Ajustando por ruido ambiente (1 segundo)...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("¡Habla ahora! (Tienes 5 segundos)")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
        print("Audio capturado. Procesando...")
        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Resultado: {texto}")
    except sr.WaitTimeoutError:
        print("Error: Se agotó el tiempo de espera. No se detectó ningún sonido lo suficientemente alto.")
    except sr.UnknownValueError:
        print("Error: No se entendió el audio. Puede que haya mucho ruido o el micrófono no capte bien tu voz.")
    except Exception as e:
        print(f"Error inesperado: {type(e).__name__} - {e}")

if __name__ == '__main__':
    test_mic()
