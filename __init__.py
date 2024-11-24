from dotenv import load_dotenv 
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import time
from models import Base
from contextlib import contextmanager
from fastapi.concurrency import contextmanager_in_threadpool
from functools import wraps

load_dotenv(dotenv_path="../.env")

BACKEND_ADDR: str = os.environ['BACKEND_ADDR'] # THe backend server's address
BACKEND_PORT: int = int(os.environ['BACKEND_PORT']) # The backend server's port
BACKEND_ORIGIN: str = os.environ.get("BACKEND_ORIGIN", f'http://{BACKEND_ADDR}:{BACKEND_PORT}') # The backend's origin 

FRONTEND_ADDR: str = os.environ['FRONTEND_ADDR'] # The frontend server's address
FRONTEND_PORT: str = os.environ['FRONTEND_PORT'] # The frontend server's port
FRONTEND_ORIGIN: str = os.environ.get('FRONTEND_ORIGIN', f'http://{FRONTEND_ADDR}:{FRONTEND_PORT}') # The frontend's origin

SESSION_DURATION = 30 * 60

SALT = "tK3K946fVn84Eap0W5pHB2fL"

engine = create_engine(f"sqlite:///database.db")
    
SessionLocal = sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)

metadata = MetaData()
metadata.reflect(bind=engine)
tableCount: int = len(metadata.tables)

def getDb():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def getAsyncDbSession(func):
    """Decorator will be used to create and use asynchronous db sessions"""
    @wraps(func)
    async def wrapperFunc(*args, **kwargs):
        async with contextmanager_in_threadpool(contextmanager(getDb)()) as session:
            kwargs.update({"session":session})
            return await func(*args, **kwargs)
        
    return wrapperFunc

if not tableCount > 0:
    Base.metadata.create_all(bind=engine)