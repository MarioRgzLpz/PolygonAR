import cv2
import numpy as np
import camara as camara  # Suponiendo que aquí importas tus configuraciones de cámara
import math

def num_lados(poligono):
    poligonos = {
        "Triangulo": 3, "Cuadrilatero": 4, "Pentagono": 5, "Hexagono": 6,
        "Heptagono": 7, "Octagono": 8, "Eneagono": 9, "Decagono": 10,
        "Undecagono": 11, "Dodecagono": 12
    }
    return poligonos.get(poligono, 0)

def obtener_vertices(cx, cy, radio, n, angulo_inicial=0):
    vertices = []
    for i in range(n):
        angle = angulo_inicial + 2 * math.pi * i / n
        x = int(cx + radio * math.cos(angle))
        y = int(cy + radio * math.sin(angle))
        vertices.append((x, y))
    return vertices

def pintar_poligono(frame, vertices, color):
    vertices_np = np.array([vertices], dtype=np.int32)
    cv2.fillPoly(frame, vertices_np, color)

def pintar_aristas(frame, vertices, color):
    n = len(vertices)
    for i in range(n):
        cv2.line(frame, vertices[i], vertices[(i + 1) % n], color, 1)

def pintar_prisma(frame, vertices, altura, color):
    vertices_superiores = [(x, y - altura) for (x, y) in vertices]
    n = len(vertices)
    
    # Dibujar aristas laterales visibles
    for i in range(n):
        # Calcular el vector normal al plano formado por los vértices i e i+1
        vec1 = np.array(vertices[i]) - np.array(vertices[(i + 1) % n])
        vec2 = np.array(vertices_superiores[i]) - np.array(vertices[i])
        normal = np.cross(vec1, vec2)

        # Verificar la orientación de la normal respecto al punto de vista (cámara)
        dot_product = np.dot(normal, np.array([0, 0, 1]))
        if np.any(dot_product < 0):
            # Rellenar la cara lateral si algún elemento de dot_product es menor que 0
            pintar_poligono(frame, [vertices[i], vertices[(i + 1) % n], vertices_superiores[(i + 1) % n], vertices_superiores[i]], color)
            # Dibujar la arista entre los vértices i y i+1
            cv2.line(frame, vertices[i], vertices_superiores[i], (0, 0, 0), 1)
    
    # Dibujar aristas de la base inferior en negro solo si son visibles
    for i in range(n):
        # Calcular el vector normal al plano formado por los vértices i e i+1
        vec1 = np.array(vertices[i]) - np.array(vertices[(i + 1) % n])
        vec2 = np.array(vertices_superiores[i]) - np.array(vertices[i])
        normal = np.cross(vec1, vec2)

        # Verificar la orientación de la normal respecto al punto de vista (cámara)
        dot_product = np.dot(normal, np.array([0, 0, 1]))
        if np.any(dot_product < 0):
            # Dibujar la arista solo si algún elemento de dot_product es menor que 0
            cv2.line(frame, vertices[i], vertices[(i + 1) % n], (0, 0, 0), 1)

    # Rellenar polígono de la base superior 
    pintar_poligono(frame, vertices_superiores, color)

    # Dibujar aristas superiores visibles en el color especificado
    for i in range(n):
        # Calcular el vector normal al plano formado por los vértices i e i+1
        vec1 = np.array(vertices[i]) - np.array(vertices[(i + 1) % n])
        vec2 = np.array(vertices_superiores[i]) - np.array(vertices[i])
        normal = np.cross(vec1, vec2)

        # Verificar la orientación de la normal respecto al punto de vista (cámara)
        dot_product = np.dot(normal, np.array([0, 0, 1]))
        if np.any(dot_product < 0):
            # Dibujar la arista solo si algún elemento de dot_product es menor que 0
            cv2.line(frame, vertices[i], vertices_superiores[i], (0, 0, 0), 1)

        # También dibujar la arista entre el último y el primer vértice para cerrar la base
        if i == n - 1:
            if np.any(dot_product < 0):
                cv2.line(frame, vertices[0], vertices_superiores[0], (0, 0, 0), 1)

    pintar_aristas(frame, vertices_superiores, (0, 0, 0))

def pintar_piramide(frame, vertices, altura, color):
    cx, cy = np.mean(vertices, axis=0).astype(int)
    vertice_superior = (cx, cy - altura)
    n = len(vertices)
    
    # Rellenar polígono de la base
    pintar_poligono(frame, vertices, color)

    # Dibujar aristas de la base en negro solo si son visibles
    for i in range(n):
        # Calcular el vector normal al plano formado por los vértices i e i+1
        vec1 = np.array(vertices[i]) - np.array(vertices[(i + 1) % n])
        vec2 = np.array(vertice_superior) - np.array(vertices[i])
        normal = np.cross(vec1, vec2)

        # Verificar la orientación de la normal respecto al punto de vista (cámara)
        dot_product = np.dot(normal, np.array([0, 0, 1]))
        if np.any(dot_product < 0):
            # Dibujar la arista solo si algún elemento de dot_product es menor que 0
            cv2.line(frame, vertices[i], vertices[(i + 1) % n], (0, 0, 0), 1)

    # Dibujar aristas laterales visibles en el color especificado
    for i in range(n):
        # Calcular el vector normal al plano formado por los vértices i y el vértice superior
        vec1 = np.array(vertices[i]) - np.array(vertice_superior)
        vec2 = np.array(vertices[(i + 1) % n]) - np.array(vertices[i])
        normal = np.cross(vec1, vec2)

        # Verificar la orientación de la normal respecto al punto de vista (cámara)
        dot_product = np.dot(normal, np.array([0, 0, 1]))
        if np.any(dot_product < 0):
            # Rellenar la cara lateral si algún elemento de dot_product es menor que 0
            pintar_poligono(frame, [vertices[i], vertices[(i + 1) % n], vertice_superior], color)
        
        # Dibujar la arista solo si algún elemento de dot_product es menor que 0
        cv2.line(frame, vertices[i], vertice_superior, (0, 0, 0), 1)


def pintar_3d(frame, poligono, modo, altura, color):
    DICCIONARIO = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
    detector = cv2.aruco.ArucoDetector(DICCIONARIO)
    tamano_real = 8
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    corners, ids, _ = detector.detectMarkers(gris)
    if ids is not None:
        for i in range(len(ids)):
            rvec, tvec, marker = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, camara.cameraMatrix, camara.distCoeffs)
            (rvec - tvec).any()
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            c_x = int((corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]) / 4)
            c_y = int((corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]) / 4)
            
            # Calcular el radio como la mayor distancia desde el centro a las esquinas
            radios = [
                int(math.sqrt((corners[0][0][0][0] - c_x)**2 + (corners[0][0][0][1] - c_y)**2)),
                int(math.sqrt((corners[0][0][1][0] - c_x)**2 + (corners[0][0][1][1] - c_y)**2)),
                int(math.sqrt((corners[0][0][2][0] - c_x)**2 + (corners[0][0][2][1] - c_y)**2)),
                int(math.sqrt((corners[0][0][3][0] - c_x)**2 + (corners[0][0][3][1] - c_y)**2))
            ]
            radio = max(radios)

            # Calcular el ángulo inicial para mantener el primer vértice fijo
            angulo_inicial = math.atan2(corners[0][0][0][1] - c_y, corners[0][0][0][0] - c_x)
            
            # Obtener el número de lados del polígono
            n = num_lados(poligono)
            
            # Obtener los vértices del polígono
            vertices = obtener_vertices(c_x, c_y, radio, n, angulo_inicial)

            # Añadir la altura al polígono
            marcador_size = int(math.sqrt((corners[0][0][0][0] - corners[0][0][2][0])**2 + (corners[0][0][0][1] - corners[0][0][2][1])**2))
            altura_en_pixeles = int(marcador_size * altura / tamano_real)
            
            # Pintar el polígono en la imagen
            if modo == "prisma":
                pintar_prisma(frame, vertices, altura_en_pixeles, color)
            elif modo == "piramide":
                pintar_piramide(frame, vertices, altura_en_pixeles, color)
            
            # Calcular la posición del texto en el centro elevado a una altura
            text_height = c_y - altura_en_pixeles - 10  
            cv2.putText(frame, poligono, (c_x, text_height), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        pintar_3d(frame, "Cuadrilatero", "piramide", 10, (255, 0, 0))  
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
