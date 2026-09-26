import threading
import time

def background_monitor():
    while True:
        print("[Daemon] Listening for incoming background signals...")
        time.sleep(1)

# Set daemon=True so this thread won't hold the program open
monitor_thread = threading.Thread(target=background_monitor, daemon=True)
monitor_thread.start()

print("Main program doing short work...")
time.sleep(2.5)
print("Main program finished! Exiting now...")

# At this point, the main thread terminates, and monitor_thread is killed immediately.