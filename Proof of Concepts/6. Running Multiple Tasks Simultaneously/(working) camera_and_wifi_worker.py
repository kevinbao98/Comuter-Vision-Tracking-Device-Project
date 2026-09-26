import threading
import time
import cv2

def camera_stream_worker():
    """Worker process dedicated to capturing and processing camera frames."""
    cap = cv2.VideoCapture(0)
   
    while True:
        # 1. Grab frame from camera (e.g., cv2.VideoCapture)
        # 2. Run vision algorithm / tracking
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            '''
            NOTE: 
            1. Very important to have this if statement otherwise the camera window will be a blank frame
            2. cv2.imshow() because it blocks input() in command_transmitter(), because of how OpenCV manges GUI events. cv2 relies on cv2.waitKey() to run a continuous loop
            '''
            break
    cap.release()
    cv2.destroyAllWindows()

def command_transmitter():
    while True:
        try:
            servo_speed = input("Enter servo speed: ")
            time.sleep(1)
            print(f"------> Sending servo_speed = {servo_speed}")    
        except EOFError:    
            break
        print("<------ Client recieved servo_speed!\n")    
        
if __name__ == "__main__":
    '''
    Daemon is a non-blocking background thead. If set to true, that thread will stop if main thread stops
    '''
    input_thread = threading.Thread(target=command_transmitter, daemon=False) 
    camera_thread = threading.Thread(target=camera_stream_worker, daemon=True) 
    input_thread.start()
    camera_thread.start()