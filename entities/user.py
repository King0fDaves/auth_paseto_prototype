from crud.user import UserCRUD
from __init__ import getAsyncDbSession
import uuid
from models import User

class User:

    @getAsyncDbSession
    async def __call__(self, session, payload) -> User:
        userId = uuid.UUID(payload['user_id'])
        user = UserCRUD.readUserById(session=session, id=userId)
        return user