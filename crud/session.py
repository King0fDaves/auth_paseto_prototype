from .crud import CRUD
from models import Session
import uuid
from datetime import datetime

class SessionCRUD(CRUD):

    @classmethod
    def createSession(cls, 
        session, id: str, 
        tokenId: uuid.UUID = None,
        userId: uuid.UUID = None, 
        expiresAt: datetime = None
    ) -> Session:
        """Creates a Session record"""
        newSession = Session(
            id=id, token_id=tokenId,
            user_id=userId, expires_at=expiresAt
        )
        return cls.save(db=session, model=newSession)

    @staticmethod
    def readSessionById(session, id: uuid.UUID) -> Session:
        """Reads a Session record by its id"""
        account: Session = session.query(Session).filter(Session.id == id).first()
        return account
    
    @staticmethod
    def readSessionByTokenId(session, tokenId: uuid.UUID) -> Session:
        """Reads a Session record by its token id"""
        account: Session = session.query(Session).filter(Session.token_id == tokenId).first()
        return account