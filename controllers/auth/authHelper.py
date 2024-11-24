from tokens import Tokens
from schemas.auth import AuthToken, Tokens as STokens
from passlib.context import CryptContext
import random, string, uuid
from datetime import datetime, timedelta
from __init__ import SESSION_DURATION

class AuthHelper: 
    
    bcryptContext = CryptContext(schemes=['bcrypt'], deprecated="auto")

    @classmethod
    def createAuthTokens(cls, userId: uuid.UUID, sessionId: str) -> STokens:
        """Creates the nessecary auth tokens for the user"""

        clientSecret = cls.generateClientSecret()
        secretKey = str(sessionId[16:]) + clientSecret 

        tokenKey = Tokens.createKey(secretKey)
        wrappedTokenKey = Tokens.wrapKey(key=tokenKey, secretKey=secretKey)

        tokenId = uuid.uuid4()

        authToken = AuthToken(user_id=str(userId), jti=str(tokenId))
        token = Tokens.createToken(key=tokenKey, payload=dict(authToken), expSecs=SESSION_DURATION)

        return STokens(
            token_key=wrappedTokenKey, token=token.decode(), 
            client_secret=clientSecret, token_id=tokenId
        )

    @classmethod
    def generateClientSecret(cls, keyLength: int = 12):
        
        secret = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) 
            for _ in range(keyLength)
        )
        return secret

    @staticmethod
    def generateExpSessionTimestamp():
        return datetime.now() + timedelta(seconds=SESSION_DURATION)