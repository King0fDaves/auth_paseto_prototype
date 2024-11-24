from dataclasses import dataclass
from starlette import status
from typing import Callable
from fastapi import Request, HTTPException
from starlette.responses import JSONResponse

@dataclass
class BaseError(Exception):
    """Base exception class"""
    message: str

@dataclass
class BadRequestError(BaseError):
    """Catch-all status code error"""
    status = status.HTTP_400_BAD_REQUEST

@dataclass
class NotFoundError(BaseError):
    """Error for not found resource"""
    status = status.HTTP_404_NOT_FOUND

@dataclass
class InputFormError(BaseError):
    """Error for improper user input"""
    status = status.HTTP_422_UNPROCESSABLE_ENTITY

@dataclass
class ConflictError(BaseError):
    """Error for conflicted operations"""
    status = status.HTTP_409_CONFLICT

@dataclass
class DeniedError(BaseError):
    """Error for denied operations"""
    status = status.HTTP_403_FORBIDDEN

@dataclass
class AuthenticationError(BaseError):
    """Error for unauthenticated requests"""
    status = status.HTTP_401_UNAUTHORIZED

def createExceptionHandler() -> Callable[[Request, BaseError], JSONResponse]:
    """Will return an exception handler function"""
    async def exceptionHandler(_: Request, exception: BaseError) -> JSONResponse:
        """Raise an http exception with error status code and message"""
        raise HTTPException(status_code=exception.status, detail=exception.message)
    return exceptionHandler
