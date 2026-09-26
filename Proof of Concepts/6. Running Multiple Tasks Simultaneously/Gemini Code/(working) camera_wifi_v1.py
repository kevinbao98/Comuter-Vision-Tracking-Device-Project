import cv2
import threading

# Shared variables between threads
servo_speed = 50
running = True

def console_input_loop():
    """Runs in a background thread to accept terminal input without blocking OpenCV."""
    global servo_speed, running
    
    while running:
        try:
            user_val = input("Enter new servo speed (0-100): ")
            if user_val.isdigit():  
                servo_speed = int(user_val)
                print(f"--> Speed updated to: {servo_speed}")
            else:
                print("Please enter a valid integer.")
        except (EOFError, KeyboardInterrupt):
            break

def run_camera_stream():
    """Handles camera capture, frame rendering, and OpenCV event handling."""
    global running
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        running = False
        return

    print("Camera stream started. Press 'q' in the window to quit.")

    while running:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Overlay current speed value onto the frame
        cv2.putText(frame, f"Current Speed: {servo_speed}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display camera stream window
        cv2.imshow("Camera Stream", frame)

        # Non-blocking waitKey to handle window rendering and quit event
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

    # Clean up camera locks and window GUI
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Start the input thread as a daemon so it exits automatically when main thread finishes
    input_thread = threading.Thread(target=console_input_loop, daemon=True)
    input_thread.start()

    # Run the main camera stream loop on the primary thread
    run_camera_stream()