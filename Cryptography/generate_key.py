from cryptography.fernet import Fernet

key = Fernet.generate_key()
key_file = open("encryption_key.txt", "wb")
key_file.write(key)
key_file.close()
