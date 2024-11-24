from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from encrypts import Encrypts
from __init__ import getAsyncDbSession
from crud.session import SessionCRUD
import uuid
from errors import AuthenticationError
from datetime import datetime

class SessionMiddleware(BaseHTTPMiddleware):
    """Middleware for generating client session id"""

    def __init__(self, app):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next) -> Request:
        try:
            clientIds = (request.client.host, request.headers['user-agent'])
            sessionId = Encrypts.generateHash(values=clientIds)

            headers = dict(request.scope['headers'])
            headers.update({b"session-id":f"{sessionId}".encode()})
            headers = [(k, v) for k, v in headers.items()]
            request.scope.update({"headers":headers})

            if "protected" in request.url.path:
                tokenId = request.cookies.get("token_id")

                if not tokenId:
                    raise AuthenticationError("Unauthenticated")
                
                await self.handleProtectedSession(tokenId=uuid.UUID(tokenId), sessionId=sessionId)
            
                return await call_next(request)
                
            await self.handlePublicSession(sessionId=sessionId)

            return await call_next(request)
        
        except AuthenticationError as error:
             return JSONResponse(status_code=401, content={"detail":f"{error}"})

    @staticmethod
    @getAsyncDbSession
    async def handlePublicSession(session, sessionId):
        """Manages public sessions"""

        foundSession = SessionCRUD.readSessionById(session=session, id=sessionId)

        if not foundSession:
            SessionCRUD.createSession(session=session, id=sessionId, userId=uuid.uuid4())
    
    @staticmethod
    @getAsyncDbSession
    async def handleProtectedSession(session, tokenId: uuid.UUID, sessionId:str):
        """Manages authenticated sessions"""

        userSession = SessionCRUD.readSessionByTokenId(session=session, tokenId=tokenId)

        if not userSession:
            raise AuthenticationError("Unauthenticated")

        if userSession.id != sessionId:
            raise AuthenticationError("Unauthenticated")
        
        if  datetime.now() >= userSession.expires_at:
            SessionCRUD.delete(db=session, model=userSession)
            raise AuthenticationError("Unauthenticated")