import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from __init__ import SALT

class Encrypts:
    """This will contain cryptographic functions for the application"""

    @staticmethod
    def generateKey(password: str) -> bytes:
        """Generates an encryption key"""

        passwordBytes = password.encode()
        saltBytes = SALT.encode()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=saltBytes,
            iterations=480000
        )
        key = base64.urlsafe_b64encode(kdf.derive(passwordBytes))
        return key

    @staticmethod 
    def encryptString(value: str, key: bytes) -> str:
        """Encrypts string"""
        
        fernet = Fernet(key)
        token = fernet.encrypt(value.encode())
        return token.decode()

    @staticmethod
    def decryptString(token: str, key: bytes) -> str:
        """Decrypts encrypted strings"""

        fernet = Fernet(key)
        decryptedString = fernet.decrypt(token.encode())
        return decryptedString.decode()

    @staticmethod
    def generateHash(values: tuple[str]):
        """Generates hashes from valuess"""

        digests = hashes.Hash(hashes.SHA256())
            
        digests.update(data=SALT.encode())

        for value in values:
            digests.update(data=value.encode())
            
        return digests.finalize().hex()