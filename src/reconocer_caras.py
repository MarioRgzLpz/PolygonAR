import cv2
import face_recognition

def encode_faces(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_encodings = face_recognition.face_encodings(rgb_image)
    return face_encodings

def authenticate_user(image, user_data):
    face_encodings = encode_faces(image)
    if len(face_encodings) == 0:
        return None

    for user_info in user_data.values():
        known_face_encoding = user_info['encoding']
        # Verificar que la codificación facial almacenada no esté vacía
        if known_face_encoding and len(known_face_encoding) > 0:
            matches = face_recognition.compare_faces([known_face_encoding], face_encodings[0])
            if matches[0]:
                return user_info  # Retorna el diccionario completo de user_info si hay coincidencia

    return None  # Retorna None si no se encuentra ninguna coincidencia o la codificación es inválida

def register_user(image, username, language, user_data_manager):
    face_encodings = encode_faces(image)
    if len(face_encodings) == 0:
        raise Exception("No se encontró ningún rostro en la imagen.")
    user_data_manager.add_user(username, language, face_encodings[0])