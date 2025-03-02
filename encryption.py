from cryptography.fernet import Fernet

def load_key():
    """Load the previously generated key."""
    return open("secret.key", "rb").read()

def encrypt_message(message):
    """Encrypt the secret message."""
    key = load_key()
    cipher = Fernet(key)
    return cipher.encrypt(message.encode())

def decrypt_message(encrypted_message):
    """Decrypt the hidden message."""
    key = load_key()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_message).decode()
