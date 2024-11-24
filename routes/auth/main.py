from __init__ import BACKEND_ORIGIN, FRONTEND_ORIGIN, getDb
from fastapi import FastAPI, Depends
from middleware import SessionMiddleware
from tokens import Tokens
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from schemas.user import User
from errors import *
from schemas.auth import LoginRequest, RegisterRequest
from controllers.auth.authController import AuthController
from entities.user import User as EUser
from typing import Annotated
from pyseto.exceptions import VerifyError

authApp = FastAPI()

origins = [
    FRONTEND_ORIGIN,
    BACKEND_ORIGIN
]

authApp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

authApp.add_middleware(SessionMiddleware)

authApp.add_exception_handler(
    exc_class_or_status_code=BadRequestError,
    handler=createExceptionHandler()
)

authApp.add_exception_handler(
    exc_class_or_status_code=InputFormError,
    handler=createExceptionHandler()
)

authApp.add_exception_handler(
    exc_class_or_status_code=NotFoundError,
    handler=createExceptionHandler()
)

authApp.add_exception_handler(
    exc_class_or_status_code=AuthenticationError,
    handler=createExceptionHandler()
)

authApp.add_exception_handler(
    exc_class_or_status_code=ConflictError,
    handler=createExceptionHandler()
)

authApp.add_exception_handler(
    exc_class_or_status_code=DeniedError,
    handler=createExceptionHandler()
)

async def getSessionId(request: Request):
    sessionId = request.headers.get('session-id')
    return sessionId

async def getCurrentUser(request: Request):
    try:
        sessionId = request.headers.get("session-id")
        clientSecret = request.cookies.get("client_secret")
        tokenKey = request.cookies.get("token_key")
        token = request.cookies.get("token")

        secretKey = sessionId[16:] + clientSecret 
        tokenKey = Tokens.unwrapKey(wrappedKey=tokenKey, secretKey=secretKey)
        data = Tokens.revealToken(key=tokenKey, token=token)
        return data
    except VerifyError:
        raise AuthenticationError("Unauthenticated")

sessionIdDepedency =  Annotated[dict, Depends(getSessionId)]

async def getTokenPayload(request: Request):
    """Decrpyts the token and extracts its payload"""
    try:
        sessionId = request.headers.get("session-id")
        clientSecret = request.cookies.get("client_secret")
        tokenKey = request.cookies.get("token_key")
        token = request.cookies.get("token")

        secretKey = sessionId[16:] + clientSecret 
        tokenKey = Tokens.unwrapKey(wrappedKey=tokenKey, secretKey=secretKey)
        data = Tokens.revealToken(key=tokenKey, token=token)
        return data.payload
    
    except VerifyError:
        raise AuthenticationError("Unauthenticated")

payloadDepedency = Annotated[dict, Depends(getTokenPayload)]

async def getCurrentUser(payload: payloadDepedency):
    user = EUser()
    currentUser = await user(payload=payload)
    return currentUser

userDepedency = Annotated[User, Depends(getCurrentUser)]

@authApp.post("/login")
async def login_user(
    request: LoginRequest, 
    sessionId: sessionIdDepedency,
    dbSession = Depends(getDb)
):
    tokens = AuthController.authenticateUser(
        session=dbSession,
        sessionId=sessionId,
        username=request.username,
        password=request.password
    )

    content = {"detail":"Successful login"}
    response = JSONResponse(content=content)

    for key, value in dict(tokens).items():
        response.set_cookie(key=f"{key}", value=f"{value}", httponly=True, secure=True)

    return response

@authApp.post("/register")
async def register_user(
    request: RegisterRequest,
    sessionId: sessionIdDepedency, 
    dbSession = Depends(getDb)
):

    awaitedRequest: RegisterRequest = await request
    
    tokens = AuthController.registerUser(
        session=dbSession,
        sessionId=sessionId,
        username=awaitedRequest.username,
        password=awaitedRequest.password
    )

    content = {"detail":"Successful registration"}
    response = JSONResponse(content=content)

    for key, value in dict(tokens).items():
        response.set_cookie(key=f"{key}", value=f"{value}", httponly=True, secure=True)

    return response

@authApp.delete("/logout")
async def logout_user(payload: payloadDepedency):

    await AuthController.logoutUser(tokenId=payload['jti'])
    content = {"detail":"Logout successful"}
    response = JSONResponse(content)
    return response

@authApp.get("/current-user")
async def get_current_user(user: userDepedency):
    return user