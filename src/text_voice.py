import pyttsx3

def init_engine(language='es'):
    engine = pyttsx3.init()
    # Configurar el idioma del motor de voz
    voices = engine.getProperty('voices')
    if language == 'español':
        # Seleccionar una voz en español
        for voice in voices:
            if 'spanish' in voice.id:
                engine.setProperty('voice', voice.id)
                break
    elif language == 'English':
        # Seleccionar una voz en inglés
        for voice in voices:
            if 'english' in voice.id:
                engine.setProperty('voice', voice.id)
                break
    return engine

def speak(cola_text, cola_idiomas, hablar, escuchar):
    while True:
        if not cola_text.empty():
            text = cola_text.get()
            if not cola_idiomas.empty():
                language = cola_idiomas.get()
            else:
                language = 'español'
            if text is not None:
                hablar.set()
            engine = init_engine(language)
            engine.setProperty('rate', 160)
            engine.say(text)
            engine.runAndWait()
            hablar.clear()
            


if __name__ == "__main__":
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice.id)