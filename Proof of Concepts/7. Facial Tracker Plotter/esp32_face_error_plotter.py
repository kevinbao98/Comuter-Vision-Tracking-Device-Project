import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation

esp32_cam_url = "http://192.168.0.135:81/stream"

# --- Configuration & Setup ---
# No limits data storage
time_steps = []
x_errors = []
y_errors = []

frame_count = 0
cap = cv2.VideoCapture(esp32_cam_url)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Setting up plot size and legend
fig, ax = plt.subplots(figsize=(8, 4))
line_x, = ax.plot([], [], label="X Error (Horizontal)", color="crimson", lw=1.5)
line_y, = ax.plot([], [], label="Y Error (Vertical)", color="royalblue", lw=1.5)

ax.set_title("Facial Tracking Error Data (Live)")
ax.set_xlabel("Frames Since Start")
ax.set_ylabel("Error (Pixels)")
ax.axhline(0, color='gray', linestyle='--', alpha=0.5) # Axis horizontal line at y=0
ax.legend(loc="upper left")
ax.grid(True, alpha=0.3)

# Initial view limits
ax.set_xlim(0, 100)
ax.set_ylim(-300, 300)

def init():
     # Initialize the lines for the animation
     line_x.set_data([], [])
     line_y.set_data([], [])
     return line_x, line_y


def update(frame):
    global frame_count

    ret, frame = cap.read()
    if (ret):
        frame = cv2.flip(frame, 0)
        height, width, _ = frame.shape
        screen_center_x = width//2
        screen_center_y = height//2
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors=5, minSize=(30,30))         )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_center_x = x + (w // 2)
            face_center_y = y + (h // 2)
        
            cv2.circle(frame, (face_center_x, face_center_y), 5, (0, 0, 255), -1)
            
            error_x = face_center_x - screen_center_x
            error_y = face_center_y - screen_center_y
            # Plot the errors

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

ani = animation.FuncAnimation(fig, update, init_func=init, blit=False, interval=33, cache_frame_data = False)

plt.show()

cap.release()
cv2.destroyAllWindows()
