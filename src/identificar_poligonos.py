import cv2
import numpy as np

# Inicializar la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break


    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gris, (3, 3), 0)
    canny = cv2.Canny(blurred, 50,50)
    contornos, jerarquía = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contornos:
        area = cv2.contourArea(c)
        print("Area: ", area)
        if area > 2000: #Descartamos polígonos de menos de 3 lados
            M=cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
            cv2.polylines(frame, [c], True, color=(100,100,255), thickness=3)
            perimetro = cv2.arcLength(c, True )
            approx = cv2.approxPolyDP(c, perimetro*0.2, True)
            num_lados = len(approx)
            if num_lados == 3:
                print("Triángulo")
            elif num_lados == 4:
                print("Cuadrilátero")
            elif num_lados == 5:
                print("Pentágono")
            elif num_lados == 6:
                print("Hexágono")

    cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()




