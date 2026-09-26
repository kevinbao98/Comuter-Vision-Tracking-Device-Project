import serial

MAX_BUFF_LEN = 255

port = serial.Serial("COM3", 115200, timeout=1) # This is where the python communicates with arduino

# Reads one char; Not sure how this works
def read_ser(num_char = 1):
    string = port.read(num_char)
    return string.decode()

def write_ser(cmd):
    cmd = cmd + '\n'
    port.write(cmd.encode())

while (1):
    string = read_ser(MAX_BUFF_LEN) # What is this?
    if(len(string)):
        print(string)

    cmd = input() # Takes in input
    if(cmd):
        write_ser(cmd)