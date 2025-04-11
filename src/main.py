import cv2
from user_data import UserData
from reconocer_caras import authenticate_user, register_user
from text_voice import speak
from voice_recognition import detect
import traducciones
import threading
import queue
from voice_comprobations import procesar_idioma, procesar_nombre, procesar_modo, procesar_altura, procesar_color
from reconocer_poligonos import detectar_poligonos
from pintar_poligonos import pintar_3d

def manejar_evento(evento,cap,frame):
    while evento.is_set():
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()

def añadir_idioma(cola_idiomas1, cola_idiomas2, idioma):
    cola_idiomas1.put(idioma)
    cola_idiomas2.put(idioma)

def main():
    datos_usuario = UserData()
    cap = cv2.VideoCapture(0)
    cola_hablar = queue.Queue()
    cola_idiomas = queue.Queue()
    cola_idiomas2 = queue.Queue()
    cola_escuchar = queue.Queue()
    hablar = threading.Event()
    escuchar = threading.Event()
    hablar.clear()
    escuchar.clear()
    hilo_hablar = threading.Thread(target=speak, daemon=True, args=(cola_hablar, cola_idiomas, hablar, escuchar))
    hilo_hablar.start()
    hilo_escuchar = threading.Thread(target=detect, daemon=True, args=(cola_escuchar, cola_idiomas2, escuchar, hablar))
    hilo_escuchar.start()
    inicio_sesion = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if not inicio_sesion:
            usuario = authenticate_user(frame, datos_usuario.get_user_data())
            if usuario:
                translations = traducciones.load_translations(usuario["language"])
                inicio_sesion = True
                añadir_idioma(cola_idiomas, cola_idiomas2, usuario["language"])
                cola_hablar.put(translations['login_message'].format(username = usuario['username']))
                manejar_evento(hablar,cap,frame)
            else:
                escuchar.clear()
                cola_hablar.put("Usuario no autenticado. Registrando nuevo usuario. Por favor, diga su idioma")
                manejar_evento(hablar,cap,frame)
                escuchar.set()
                language = None
                while language is None:
                    cv2.imshow('Processed Frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                    ret, frame = cap.read()
                    if not cola_escuchar.empty():
                        language = cola_escuchar.get()
                        if procesar_idioma(language):
                            escuchar.clear()
                            añadir_idioma(cola_idiomas, cola_idiomas2, language)
                            translations = traducciones.load_translations(language)
                            cola_hablar.put(translations['register_prompt1'])
                            manejar_evento(hablar,cap,frame)
                            escuchar.set()
                            nombre = None
                            while nombre is None:
                                cv2.imshow('Processed Frame', frame)
                                if cv2.waitKey(1) & 0xFF == ord('q'):
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return
                                ret, frame = cap.read()
                                if not cola_escuchar.empty():
                                    nombre = cola_escuchar.get()
                                    escuchar.clear()
                                    if procesar_nombre(nombre):
                                        register_user(frame, nombre, language, datos_usuario)
                                        usuario = authenticate_user(frame, datos_usuario.get_user_data())
                                        añadir_idioma(cola_idiomas, cola_idiomas2, language)
                                        cola_hablar.put(translations['register_prompt2'].format(username = usuario['username']))
                                        manejar_evento(hablar, cap, frame)
                                        inicio_sesion = True
                                    else:
                                        nombre = None
                                        escuchar.clear()
                                        añadir_idioma(cola_idiomas, cola_idiomas2, language)
                                        cola_hablar.put(translations['register_error'])
                                        manejar_evento(hablar, cap, frame)
                                        escuchar.set()

                        else:
                            escuchar.clear()
                            language = None
                            cola_hablar.put("Idioma no soportado. Por favor, diga su idioma.")
                            manejar_evento(hablar, cap, frame)
                            escuchar.set()
            ret, frame = cap.read()
        else:
            escuchar.clear()   
            translations = traducciones.load_translations(usuario["language"])
            añadir_idioma(cola_idiomas, cola_idiomas2, usuario["language"])
            cola_hablar.put(translations['mode_question'])
            manejar_evento(hablar, cap, frame)
            escuchar.set()
            modo = None
            while modo is None:
                cv2.imshow('Processed Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                ret, frame = cap.read()
                if not cola_escuchar.empty():
                    modo = cola_escuchar.get()
                    escuchar.clear()
                    if procesar_modo(modo) == 'detectar':
                        modo = "detectar"
                    elif procesar_modo(modo) == 'pintar':
                        modo = "pintar"
                    elif procesar_modo(modo) == 'galeria':
                        modo = "galeria"
                    else:
                        añadir_idioma(cola_idiomas, cola_idiomas2, usuario["language"])
                        cola_hablar.put(translations['mode_unsupported'])
                        manejar_evento(hablar, cap, frame)
                        escuchar.set()
                        modo = None
            if modo == "detectar":
                ret, frame = cap.read()
                poligono = detectar_poligonos(frame)
                if poligono is not None:
                    datos_usuario.add_polygon(usuario['user_id'], poligono)
                cv2.imshow('Processed Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            elif modo == "pintar":
                pintar = True
                counter = 0
                altura = 10
                color = (255, 255, 255)
                modo_pintar = "prisma"
                while pintar:
                    escuchar.set()
                    if not cola_escuchar.empty():
                        comando = cola_escuchar.get()
                        escuchar.clear()
                        if comando is not None:
                            if "siguiente" in comando or "next" in comando:
                                counter = ((counter + 1) % len(usuario['polygons']))
                            elif "pirámide" in comando or "pyramid" in comando:
                                modo_pintar = "piramide"
                            elif "prisma" in comando or "prism" in comando:
                                modo_pintar = "prisma"
                            elif "salir" in comando or "exit" in comando:
                                pintar = False
                                break
                            elif "altura" in comando or "height" in comando:
                                altura = procesar_altura(comando)
                            elif "color" in comando:
                                color = procesar_color(comando)
                                print(color)

                    ret, frame = cap.read()
                    dict_poligonos = usuario['polygons']
                    poligonos = []
                    for key in dict_poligonos:
                        poligonos.append(dict_poligonos[key])
                    if len(poligonos) > 0:
                        pintar_3d(frame, poligonos[counter], modo_pintar, altura, color)
                    cv2.imshow('Processed Frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                escuchar.clear()
            elif modo == "galeria":
                dict_poligonos = usuario['polygons']
                poligonos = []
                for key in dict_poligonos:
                    poligonos.append(dict_poligonos[key])
                print("Tu galeria es la siguiente:")
                for poligono in poligonos:
                    print(poligono)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
