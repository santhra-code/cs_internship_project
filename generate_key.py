from cryptography.fernet import Fernet

# Generate and save encryption key
key = Fernet.generate_key()
with open("secret.key", "wb") as key_file:
    key_file.write(key)

print("Encryption key saved as 'secret.key'.")
