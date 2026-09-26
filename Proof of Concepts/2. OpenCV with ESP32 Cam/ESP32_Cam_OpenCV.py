import cv2

url = "http://192.168.0.123:81/stream" # Corresponding Arduino File: D:\Control Systems Engineering\Facial Tracker Project\OpenCV_Tracker\CameraWebServer
cap = cv2.VideoCapture(url)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    ret, frame = cap.read()
    if (ret):
        # cv2.imshow("Original Frame", frame)
        # inverted = cv2.bitwise_not(frame)
        # cv2.imshow("Inverted Frame", inverted)
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        screen_center_x = width//2
        screen_center_y = height//2
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors=5,
            minSize=(30,30)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_center_x = x + (w // 2)
            face_center_y = y + (h // 2)
        
            cv2.circle(frame, (face_center_x, face_center_y), 5, (0, 0, 255), -1)
            
            error_x = face_center_x - screen_center_x
            error_y = face_center_y - screen_center_y

            # Display offsets
            cv2.putText(frame, f"Offset X: {error_x} Y {error_y}", (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
            break # Tracking one face to prevent bbox from jumping
        cv2.imshow("Frame", frame)
    else:
        print("No frame found")
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()