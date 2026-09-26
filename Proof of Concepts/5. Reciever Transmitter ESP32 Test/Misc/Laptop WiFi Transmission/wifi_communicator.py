import socket
import sys
import threading

ESP32_IP = ""
PORT = "8888"
def receieve_feedback(sock):
    # Listens for confimation mesages back from the ESP32
    while True:
        try:
            data = sock.recv(1024) # What is this?
            if not data:
                print("Connection closed by ESP32.")
                break
            # Printing feedback from ESP32 to the terminal console
            sys.stdout.write(data.decode('utf-8', erros="ignore"))
            sys.stdout.flush()
        except socket.error:
            break
    
def main():
    # Setup socket using the AF_INET (IPv4) address family and the TCP protocol
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Connection to ESP32 Servo Server at {ESP32_IP}:{PORT}...")
    try:
        client_socket.connect((ESP32_IP, PORT))
        print("Connected Successfully!")
    except socket.error as e:
        print("Connection failed: {e}")
        return
    
    feedback_thread = threading.Thread(target=receive_feedback, args=(client_socket,), daemon=True)
    feedback_thread.start() 

    print("\nEnter an angle between 0 and 360 (or Ctrl+C to quit):")
    try:
        while True:
            user_input = input("Target Angle > ")
            if user_input.strip():
                command = f"{user_input}"
                client_socket.sendall(command.encode('utf-8'))
    except KeyboardInterrupt:
        print("\nExiting and closing connection.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()