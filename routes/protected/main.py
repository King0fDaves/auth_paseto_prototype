from __init__ import BACKEND_ORIGIN, FRONTEND_ORIGIN
from fastapi import FastAPI
from middleware import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from errors import *
from schemas.user import User as SUser
from .tasks import router as tasksRouter
from ..auth.main import userDepedency

protectedApp = FastAPI()

origins = [
    FRONTEND_ORIGIN,
    BACKEND_ORIGIN
]

protectedApp.include_router(tasksRouter)

protectedApp.add_middleware(SessionMiddleware)

protectedApp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

protectedApp.add_exception_handler(
    exc_class_or_status_code=BadRequestError,
    handler=createExceptionHandler()
)

protectedApp.add_exception_handler(
    exc_class_or_status_code=InputFormError,
    handler=createExceptionHandler()
)

protectedApp.add_exception_handler(
    exc_class_or_status_code=NotFoundError,
    handler=createExceptionHandler()
)

protectedApp.add_exception_handler(
    exc_class_or_status_code=AuthenticationError,
    handler=createExceptionHandler()
)

protectedApp.add_exception_handler(
    exc_class_or_status_code=ConflictError,
    handler=createExceptionHandler()
)

protectedApp.add_exception_handler(
    exc_class_or_status_code=DeniedError,
    handler=createExceptionHandler()
)

@protectedApp.get("/current-user", response_model=SUser)
async def get_current_user(user: userDepedency):
    return user