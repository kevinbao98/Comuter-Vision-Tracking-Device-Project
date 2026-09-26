import socket
import tkinter as tk
from tkinter import ttk


class ServoWiFiClient:

    def __init__(self, ip: str, port: int = 8080): # Stores WiFi IP and the "door" it should listens to
        self.ip = ip
        self.port = port

    def send_angle(self, angle: int) -> bool:
        """Sends an angle (0-180) to the ESP32 over a TCP socket."""
        angle = max(0, min(180, int(angle))) # Keeps values within 0 and 180
        message = f"{angle}\n"

        try:
            # Opening standard internet connection (TCP socket)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0) # Give up on moves if response not within 2 sec
                s.connect((self.ip, self.port)) # Dials ESP32's IP addreess and port
                s.sendall(message.encode("utf-8")) # Coverting text andle into bytes and sends over WiFi
                return True # Signal delivery was successful
        except Exception as e:
            print(f"Failed to send command to {self.ip}:{self.port} -> {e}")
            return False # Signal delivery failed


class ServoApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Wi-Fi Servo Controller")
        self.geometry("380x300")
        self.resizable(True, True)

        # Configurable ESP32 IP
        self.esp32_ip = tk.StringVar(value="    ")
        self.client = None

        self._create_widgets() # Draw all visuals on screen

    def _create_widgets(self):
        # Connection Frame
        conn_frame = ttk.LabelFrame(self, text="Connection", padding=10)
        conn_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(conn_frame, text="ESP32 IP:").pack(side="left", padx=5)
        ttk.Entry(conn_frame, textvariable=self.esp32_ip, width=15).pack(
            side="left", padx=5
        )

        # Servo Control Frame
        control_frame = ttk.LabelFrame(self, text="Servo Angle", padding=10)
        control_frame.pack(fill="x", padx=10, pady=5)

        self.angle_label = ttk.Label(
            control_frame, text="90°", font=("Arial", 16, "bold")
        )
        self.angle_label.pack(pady=5)

        self.slider = ttk.Scale(
            control_frame,
            from_=0,
            to=180,
            orient="horizontal",
            command=self._on_slider_move,
        )
        self.slider.set(90)
        self.slider.pack(fill="x", padx=10, pady=5)

        # Quick Preset Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(pady=5)

        ttk.Button(
            btn_frame, text="0°", command=lambda: self._set_angle(0)
        ).pack(side="left", padx=5)
        ttk.Button(
            btn_frame, text="90°", command=lambda: self._set_angle(90)
        ).pack(side="left", padx=5)
        ttk.Button(
            btn_frame, text="180°", command=lambda: self._set_angle(180)
        ).pack(side="left", padx=5)

        # Status Label
        self.status_label = ttk.Label(self, text="Ready", foreground="gray")
        self.status_label.pack(side="bottom", pady=5)

    def _on_slider_move(self, val):
        angle = int(float(val))
        self.angle_label.config(text=f"{angle}°")

    def _set_angle(self, angle: int):
        self.slider.set(angle)
        self.angle_label.config(text=f"{angle}°")
        self.transmit_current_angle()

    def transmit_current_angle(self):
        angle = int(self.slider.get())
        ip = self.esp32_ip.get().strip()

        client = ServoWiFiClient(ip=ip, port=8080)
        success = client.send_angle(angle)

        if success:
            self.status_label.config(
                text=f"Sent {angle}° to {ip}", foreground="green"
            )
        else:
            self.status_label.config(
                text=f"Connection Error to {ip}", foreground="red"
            )


if __name__ == "__main__":
    app = ServoApp()

    # Add a "Send" button tied to releasing the slider
    ttk.Button(
        app, text="Send Slider Position", command=app.transmit_current_angle
    ).pack(pady=5)

    app.mainloop()