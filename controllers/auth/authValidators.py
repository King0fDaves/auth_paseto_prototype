from errors import *
from crud.user import UserCRUD
from __init__ import getAsyncDbSession

class AuthValidator:

    @staticmethod
    @getAsyncDbSession
    async def validateUsername(session, username: str) -> None:
        """Validates username for registration"""
        if not username.isalnum():
            raise InputFormError(message="Username cannot have special characters")

        if len(username) > 11:
            raise InputFormError(message="Username: maximum character length 11")

        if len(username) < 4:
            raise InputFormError(message="Username: Minimum character length 4")

        foundUser = UserCRUD.readUserByUsername(session, username)

        if foundUser:
            raise ConflictError(message="Username cannot be used")