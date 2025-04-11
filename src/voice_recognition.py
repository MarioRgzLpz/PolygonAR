import pyaudio
import sounddevice
import speech_recognition as sr

def detect(cola_voz, cola_idiomas, escuchar,hablar):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        with mic as source:
            if escuchar.is_set() and not hablar.is_set():
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                print("Processing...")
        
                language = 'es-ES'
                if not cola_idiomas.empty():
                    language = cola_idiomas.get()
                    if language == 'español':
                        language = 'es-ES'
                    elif language == 'ingles':
                        language = 'en-US'
                try:
                    text = recognizer.recognize_google(audio, language=language)
                    print(f"Google Speech Recognition thinks you said: {text}")
                except sr.UnknownValueError:
                    text = None
                except sr.RequestError as e:
                    text = None
                cola_voz.put(text)

def test():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=2)

    try:
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio, language='es-ES'))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    test()