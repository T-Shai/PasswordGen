import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def positive_hash(hashable_data : object):
    return hash(hashable_data)%(os.sys.maxsize - 1)

def encrypt(data : str, key : bytes):
    f = Fernet(key)
    data = data.encode()
    return f.encrypt(data)

def decrypt(data : bytes, key : bytes):
    f = Fernet(key)
    return f.decrypt(data)

def getKey(username, password):
    unique_id = (username+"|"+password)
    salt = unique_id.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

