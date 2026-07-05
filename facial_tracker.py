import cv2
import esp32_serial_connect as connect
print(cv2.data.haarcascades)
# Automate getting the URL
url = "http://192.168.0.158:81/stream" # Corresponding Arduino File: D:\Control Systems Engineering\Facial Tracker Project\OpenCV_Tracker\CameraWebServer
cap = cv2.VideoCapture(url)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
esp32_port = connect.set_port("COM3", 115200)

while True:
    ret, frame = cap.read()
    if (ret):
        frame = cv2.flip(frame, 1) 
        height, width, _ = frame.shape
        print(f"height: {height}, width: {width}") 
        screen_center_x = width//2
        screen_center_y = height//2
        cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 0, 255), 2) # Vertical line across the screen
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors=5, minSize=(30,30))

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
            
            # Servo steer commands
            if (error_x > 5):
                connect.write_ser(esp32_port, "0")
            elif (error_x < -5):
                connect.write_ser(esp32_port, "180")
            else:
                connect.write_ser(esp32_port, "90")

            break # Tracking one face to prevent bbox from jumping
        cv2.imshow("Frame", frame)
    else:
        print("No frame found")
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
cap.release()
cv2.destroyAllWindows()