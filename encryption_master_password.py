from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Function to generate a random salt
def generate_salt():
    # Generate a random salt
    return os.urandom(16)

# Function to derive a key from the password and salt using PBKDF2-HMAC with SHA-256
def derive_key(password, salt):
    # Derive a key from the password using PBKDF2HMAC with SHA-256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # Adjust the number of iterations as needed for your security requirements
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Function to pad data using PKCS7 padding to a multiple of the block size
def pkcs7_pad(data, block_size):
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length]) * padding_length
    return data + padding

# Function to unpad data using PKCS7 unpadding
def pkcs7_unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

# Function to encrypt the password using AES-CBC mode with PKCS7 padding
def encrypt_master_password(password, salt):
    key = derive_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES256(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_password = pkcs7_pad(password.encode(), 16)  # Pad the password to a multiple of the block size
    ct = encryptor.update(padded_password) + encryptor.finalize()
    return ct, iv

# Function to decrypt the password using AES-CBC mode with PKCS7 unpadding
def decrypt_master_password(ciphertext, iv, password, salt):
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES256(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(ciphertext) + decryptor.finalize()
    unpadded_password = pkcs7_unpad(decrypted_password)  # Unpad the decrypted password
    return unpadded_password.decode()
