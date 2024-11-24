import json
import pyseto
from pyseto import Key, KeyInterface, Paseto

class Tokens:
    
    @staticmethod
    def createKey(secretKey: str) -> KeyInterface:
        """Creates encryption key for a PASETO"""
        key = Key.new(version=4, purpose="local", key=secretKey.encode())
        return key
    
    @staticmethod
    def wrapKey(key: KeyInterface, secretKey: str) -> str:
        """Creates PASERK from an encryption key"""
        wrappedKey = key.to_paserk(password=secretKey)
        return wrappedKey

    @staticmethod
    def unwrapKey(wrappedKey: str, secretKey) -> KeyInterface:
        """Creates an ecryption key from a PASERK"""
        unwrappedKey = Key.from_paserk(paserk=wrappedKey, password=secretKey)
        return unwrappedKey

    @staticmethod
    def createToken(key: KeyInterface, payload: dict, expSecs: int):
        """Creates PASETO"""
        paseto = Paseto.new(exp=expSecs, include_iat=True)
        token = paseto.encode(key, payload, serializer=json)
        return token

    @staticmethod
    def revealToken(key: KeyInterface, token: str):
        """Decodes PASETO with encryption key""" 
        data = pyseto.decode(key, token, deserializer=json)
        return data

