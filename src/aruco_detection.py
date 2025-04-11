import cv2
import camara as camara

def detect_markers(frame):
    DICCIONARIO = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)

    detector = cv2.aruco.ArucoDetector(DICCIONARIO)

    parametros = cv2.aruco.DetectorParameters()

    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    corners, ids , _= detector.detectMarkers(gris)
    if ids is not None:
        for i in range(len(ids)):
            rvec, tvec, marker = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, camara.cameraMatrix, camara.distCoeffs)
            (rvec-tvec).any()
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.drawFrameAxes(frame, camara.cameraMatrix, camara.distCoeffs, rvec, tvec, length= 0.01)
    return frame

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read() 
        if not ret:
            break
        detect_markers(frame)
        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()