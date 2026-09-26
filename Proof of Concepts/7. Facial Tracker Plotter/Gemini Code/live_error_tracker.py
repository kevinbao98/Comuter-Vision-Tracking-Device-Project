import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Configuration & Setup ---
# Removing 'maxlen' allows arrays to grow indefinitely, retaining al
time_steps = []
x_errors = []
y_errors = []

frame_count = 0
cap = cv2.VideoCapture("http://192.168.0.135:81/stream")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- Matplotlib Figure Setup ---
fig, ax = plt.subplots(figsize=(8, 4))
line_x, = ax.plot([], [], label="X Error (Horizontal)", color="crimson", lw=1.5)
line_y, = ax.plot([], [], label="Y Error (Vertical)", color="royalblue", lw=1.5)

ax.set_title("Complete History: Face Tracking Error")
ax.set_xlabel("Frames Since Start")
ax.set_ylabel("Error (Pixels)")
ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax.legend(loc="upper left")
ax.grid(True, alpha=0.3)

# Initial view limits
ax.set_xlim(0, 100)
ax.set_ylim(-300, 300) 

def init():
    line_x.set_data([], [])
    line_y.set_data([], [])
    return line_x, line_y

def update(frame):
    global frame_count
    
    ret, img = cap.read()
    img = cv2.flip(img, 0)
    if not ret:
        return line_x, line_y
    
    
    h, w, _ = img.shape
    screen_cx, screen_cy = w // 2, h // 2
    
    cv2.drawMarker(img, (screen_cx, screen_cy), (0, 255, 0), cv2.MARKER_CROSS, 20, 2) # Target marker at center of screen
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    err_x, err_y = 0, 0
    if len(faces) > 0:
        (fx, fy, fw, fh) = faces[0]  # Explicitly grab first face array
        face_cx, face_cy = fx + (fw // 2), fy + (fh // 2)
        err_x = face_cx - screen_cx
        err_y = face_cy - screen_cy
        
        cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
        cv2.circle(img, (face_cx, face_cy), 5, (0, 0, 255), -1)
        cv2.line(img, (screen_cx, screen_cy), (face_cx, face_cy), (0, 255, 255), 2)
    # Summary: the error values are calculated based on the difference between the center of the detected face and the center of the screen. These errors are then appended to their respective lists for plotting.     
    frame_count += 1
    time_steps.append(frame_count)
    x_errors.append(err_x)
    y_errors.append(err_y)
    
    # Update the lines with total accumulated history
    line_x.set_data(time_steps, x_errors)
    line_y.set_data(time_steps, y_errors)
    
    # --- Dynamic Axis Rescaling ---
    # Expand X-axis view automatically as data grows past current boundary
    current_xmax = ax.get_xlim()[1]
    if frame_count >= current_xmax:
        ax.set_xlim(0, current_xmax + 100)
        ax.figure.canvas.draw() # Force a full chart redraw to update x-ticks
    
    # Expand Y-axis view if tracking error exceeds limits
    max_err = max(max(map(abs, x_errors), default=50), max(map(abs, y_errors), default=50))
    current_ymin, current_ymax = ax.get_ylim()
    if max_err > current_ymax:
        ax.set_ylim(-max_err - 50, max_err + 50)
        ax.figure.canvas.draw()
    
    cv2.imshow("Webcam Face Tracking (Press 'q' to Quit)", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        plt.close(fig)
        
    return line_x, line_y

# Note: blit=True is removed here because expanding axes require full redraws
ani = FuncAnimation(fig, update, init_func=init, blit=False, interval=33, cache_frame_data=False)

plt.show()

cap.release()
cv2.destroyAllWindows()