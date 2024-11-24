from datetime import datetime
from pydantic import BaseModel
import uuid

class Task(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime

class CreateTaskRequest(BaseModel):
    title: str

class UpdateTaskRequest(BaseModel):
    title: str