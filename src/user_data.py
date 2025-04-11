import json
import os

# Ruta al archivo JSON donde se almacenan los perfiles de usuario
USER_DATA_FILE = '../data/user_data.json'

class UserData:
    def __init__(self):
        self.user_data = self.load_user_data()

    def load_user_data(self):
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    print("Error: El archivo JSON está vacío o no es válido.")
                    return {}
        else:
            return {}

    def save_user_data(self):
        with open(USER_DATA_FILE, 'w') as file:
            json.dump(self.user_data, file, indent=4)

    def get_user_data(self):
        return self.user_data

    def add_user(self, username, language, face_encoding):
        next_user_id = str(len(self.user_data) + 1)  # Generar un ID único para el nuevo usuario
        user_data = {
            'user_id': next_user_id,
            'username': username,
            'language': language,
            'polygons': {},
            'encoding': face_encoding.tolist()  # Convertir el encoding a una lista para almacenarlo en JSON
        }
        self.user_data[next_user_id] = user_data
        self.save_user_data()
    
    def add_polygon(self, user_id, polygon):
        # Comprobar si el polígono ya está presente
        for existing_polygon in self.user_data[user_id]['polygons'].values():
            if existing_polygon == polygon:
                return
        
        # Si el polígono no está presente, añadirlo
        polygon_id = str(len(self.user_data[user_id]['polygons']) + 1)
        self.user_data[user_id]['polygons'][polygon_id] = polygon
        self.save_user_data()
