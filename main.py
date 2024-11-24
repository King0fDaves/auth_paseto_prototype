import os
import sys

sys.path.insert(0, os.path.abspath(".."))

from __init__ import BACKEND_PORT, BACKEND_ADDR
import uvicorn
from fastapi import FastAPI
from routes.auth.main import authApp
from routes.protected.main import protectedApp

app = FastAPI()
app.mount("/api/auth", authApp)
app.mount("/api/protected", protectedApp)

if __name__ == "__main__":
    uvicorn.run("main:app", host=BACKEND_ADDR, port=BACKEND_PORT, reload=True)
