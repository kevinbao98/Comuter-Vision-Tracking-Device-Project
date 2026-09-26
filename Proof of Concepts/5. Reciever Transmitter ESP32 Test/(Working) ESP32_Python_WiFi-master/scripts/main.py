from gui import GUI
from wifi_communicator import WiFiCommunicator

def main():
    communicator = WiFiCommunicator(max_buffer_sz=128) # Wifi communicator class initalization
    gui = GUI(communicator=communicator) # Initialzing GUI object
    gui.mainloop()

if __name__ == '__main__':
    main()
