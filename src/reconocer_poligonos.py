import cv2
import numpy as np

def detectar_poligonos(frame):
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gris, (3, 3), 0)
    canny = cv2.Canny(blurred, 50, 50)
    contornos, jerarquía = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 1500:
            approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
            num_lados = len(approx)
            print(num_lados)
            poligonos = {
                3: "Triangulo",
                4: "Cuadrilatero",
                5: "Pentagono",
                6: "Hexagono",
                7: "Heptagono",
                8: "Octagono",
                9: "Eneagono",
                10: "Decagono",
                11: "Undecagono",
                12: "Dodecagono"
            }
            print(poligonos.get(num_lados,None))
            return poligonos.get(num_lados,None)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read() 
        if not ret:
            break
        detectar_poligonos(frame)
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()