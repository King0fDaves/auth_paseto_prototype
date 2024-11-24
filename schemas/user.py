import uuid
from datetime import datetime
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    created_at: datetime

class User(BaseModel):
    id: uuid.UUID
    username: str
    created_at: datetime
