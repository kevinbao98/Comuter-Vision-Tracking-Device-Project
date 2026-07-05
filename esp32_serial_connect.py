import serial

MAX_BUFF_LEN = 255

def set_port(port, baud_rate, timeout=1):
    port = serial.Serial("COM3", 115200, timeout=1) # This is where the python communicates with arduino
    return port

def write_ser(port, cmd):
    cmd = cmd + '\n'
    port.write(cmd.encode())