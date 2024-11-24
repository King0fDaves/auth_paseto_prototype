from pydantic import BaseModel, model_validator
from controllers.auth.authValidators import AuthValidator
import uuid 

class RegisterRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode="after")
    async def validateRequest(self):
        validator = AuthValidator()
        await validator.validateUsername(username=self.username)
        return self

class LoginRequest(BaseModel): 
    username: str
    password: str

class AuthToken(BaseModel):
    iss: str = "TT_20NOV24"
    sub: str = "auth_token"
    aud: str = "registered_user"
    jti: str
    user_id: str

class Tokens(BaseModel):
    token_key: str
    token: str
    token_id: uuid.UUID
    client_secret: str