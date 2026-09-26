import socket
import time

class ServoWiFiClient:

    def __init__(self, ip, port = 8080):
        self.esp32_ip = ip
        self.esp32_port = port

    def send_msg(self, msg):
        message = msg
        print(f"------> Sent speed {message}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect((self.esp32_ip, self.esp32_port))     # Connecting to ESP32
                s.sendall(message.encode("utf-8"))  # Sending data
                print(f"<------ {message.strip()} was successfully sent!")
        except Exception as e:
            print(f"Failed to send command to IP Address {self.esp32_ip} to PORT {self.esp32_port} -> {e}")
            return False

if __name__ == "__main__":
    computer = ServoWiFiClient("192.168.4.1")

    while True:
        message = input("Enter message: ")
        computer.send_msg(message)    

