from controllers.auth.authHelper import AuthHelper
from crud.user import UserCRUD
from errors import AuthenticationError
from crud.session import SessionCRUD
import uuid
from __init__ import getAsyncDbSession

class AuthController(AuthHelper): 

    @classmethod
    def registerUser(cls, session, sessionId: str, username: str, password: str) -> None:
        """Creates a user account"""
        hashedPassword = cls.bcryptContext.hash(password)
        UserCRUD.createUser(
            session=session, 
            id=uuid.uuid4(),
            username=username,
            password=hashedPassword
        )

        tokens = cls.authenticateUser(
            session=session, 
            sessionId=sessionId, 
            username=username, 
            password=password
        )
        return tokens

    @classmethod
    def authenticateUser(cls, session, sessionId, username: str, password: str) -> dict:
        """Creates authentication tokens for the user"""

        foundUser = UserCRUD.readUserByUsername(session=session, username=username)

        if not foundUser:
            raise AuthenticationError("Incorrect credentials")
        
        if not cls.bcryptContext.verify(password, foundUser.password):
            raise AuthenticationError(message="Incorrect credentials")

        tokens = cls.createAuthTokens(userId=foundUser.id, sessionId=sessionId)
        
        if foundUser.session:
            UserCRUD.delete(db=session, model=foundUser.session)

        SessionCRUD.createSession(
            session=session, 
            id=sessionId,
            tokenId=tokens.token_id, 
            userId=foundUser.id,
            expiresAt=cls.generateExpSessionTimestamp()
        )
        return tokens

    @classmethod
    @getAsyncDbSession
    async def logoutUser(cls, session, tokenId: str) -> None:

        userSession = SessionCRUD.readSessionByTokenId(
            session=session, tokenId=uuid.UUID(tokenId)
        )

        if not userSession:
            raise AuthenticationError("Unauthenticated")
        
        SessionCRUD.delete(db=session, model=userSession) 
      
        return None