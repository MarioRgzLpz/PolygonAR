import cv2
import numpy as np
import sys
import os

cap = cv2.VideoCapture(0)
if cap.isOpened():
    final = False
    hframe = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    wframe = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("Tamaño del frame de la cámara: ", wframe, "x", hframe)

    if os.path.exists('camara.py'):
        import camara
        cameraMatrix = camara.cameraMatrix
        distCoeffs = camara.distCoeffs
        matrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (wframe,hframe), 1, (wframe,hframe))
        roi_x, roi_y, roi_w, roi_h = roi
    else:
        print("Es necesario realizar la calibración de la cámara")
        final = True

    while not final:
        ret, framebgr = cap.read()
        if ret:
            framerectificado = cv2.undistort(framebgr, cameraMatrix, distCoeffs, None, matrix)
            framerecortado = framerectificado[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
            cv2.imshow("ORIGINAL", framebgr)
            cv2.imshow("RECTIFICADO", framerectificado)
            cv2.imshow("RECORTADO", framerecortado)
            if cv2.waitKey(20) > 0:
                final = True
        else:
            final = True
else:
    print("No se pudo acceder a la cámara.")