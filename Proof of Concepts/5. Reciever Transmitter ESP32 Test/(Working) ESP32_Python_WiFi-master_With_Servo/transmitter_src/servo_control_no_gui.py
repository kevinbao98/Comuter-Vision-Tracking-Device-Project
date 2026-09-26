import socket
import time

class ServoWiFiClient:

    def __init__(self, ip: str, port: int = 8080):
        self.ip = ip
        self.port = port

    def slew_rate(self):
        None
    def send_angle(self, angle:int):
        angle = max(0, min(180, int(angle))) # max(0, ...) sets lower limit, min(180, ...) set upper limit, int(angle) makes angles whole numbers
        message = f"{angle}\n"
        print(f"Message sent was {message}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect((self.ip, self.port))     # Connecting to ESP32
                s.sendall(message.encode("utf-8"))  # Sending data
                print(f"{message.strip()} was successfully sent!")
        except Exception as e:
            print(f"Failed to send command to {self.ip} to {self.port} -> {e}")
            return False

if __name__ == "__main__":
    transmitter = ServoWiFiClient
    transmitter.ip = "192.168.1.10"
    transmitter.port = 8080

    while True:
        angle_command = input("Enter servo position: ")
        try:
            transmitter.send_angle(transmitter, angle_command)
        except:
            print(f"Angle command {angle_command} is not valid.")
        