def procesar_idioma(language):
    if language not in ['español', 'ingles', 'English', 'Spanish']:
        return False
    return True
def procesar_nombre(nombre):
    if nombre[0].islower():
        return False
    return True
def procesar_altura(altura):
    altura = altura.split(" ")
    altura = int(altura[1])
    if altura > 0:
        return altura
    else:
        return 10
    
def procesar_color(color):
    color = color.split(" ")
    color = color[1]
    colores = {
        "rojo": (0, 0, 255),
        "red": (0, 0, 255),
        "verde": (0, 255, 0),
        "green": (0, 255, 0),
        "azul": (255, 0, 0),
        "blue": (255, 0, 0),
        "amarillo": (0, 255, 255),
        "yellow": (0, 255, 255),
        "naranja": (0, 165, 255),
        "orange": (0, 165, 255),
        "rosa": (255, 105, 180),
        "pink": (255, 105, 180)
    }
    return colores.get(color.lower(), (255, 255, 255))

def procesar_modo(modo):
    if modo is not None:
        if "detectar" in modo or "detect" in modo:
            return "detectar"
        elif "pintar" in modo or "draw" in modo: 
            return "pintar"
        elif "galería" in modo or "gallery" in modo:
            return "galeria"
        else:
            return False
    return False