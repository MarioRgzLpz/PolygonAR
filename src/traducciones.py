import json
import os

TRANSLATIONS_DATA_FILE = '../data/traducciones.json'

def load_translations(lang):
    if not os.path.exists(TRANSLATIONS_DATA_FILE):
        raise FileNotFoundError(f"No se encontró el archivo de traducciones '{TRANSLATIONS_DATA_FILE}'.")
    
    with open(TRANSLATIONS_DATA_FILE, 'r', encoding='utf-8') as file:
        translations = json.load(file)
    
    if lang not in translations:
        raise KeyError(f"No se encontraron traducciones para el idioma '{lang}' en '{TRANSLATIONS_DATA_FILE}'.")
    
    return translations[lang]

def translate(key, translations, *args):
    text = translations.get(key, "")
    if args:
        text = text.format(*args)
    return text