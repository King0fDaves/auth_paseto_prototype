from .crud import CRUD
from models import User
import uuid

class UserCRUD(CRUD):

    @classmethod
    def createUser(cls, session, id: uuid.UUID, username: str, password: str):
        """Creates a User record"""
        newUser = User(id=id, username=username, password=password)
        return cls.save(db=session, model=newUser)

    @staticmethod
    def readUserByUsername(session, username: str) -> User:
        """Reads a User record by its username"""
        user: User = session.query(User).filter(User.username == username).first()
        return user
    
    @staticmethod
    def readUserById(session, id: uuid.UUID) -> User:
        """Reads a User record by its id"""
        user: User = session.query(User).filter(User.id == id).first()
        return user
    