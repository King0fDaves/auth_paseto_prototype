from .crud import CRUD
from models import Task
import uuid

class TaskCRUD(CRUD):

    @classmethod
    def createTask(cls, session, id: uuid.UUID, userId: uuid.UUID, title: str) -> Task:
        """Creates a Task record"""
        newTask = Task(id=id, user_id=userId, title=title)
        return cls.save(db=session, model=newTask)

    @staticmethod
    def readTaskByIdandUserId(session, id: int, userId: uuid.UUID) -> Task:
        """Reads a Task record by its id and the user id"""
        task: Task = session.query(Task
        ).filter(
            Task.id == id
        ).filter(
            Task.user_id == userId
        ).first()
        return task
    
    @staticmethod
    def readAllTasksByUserId(session, userId: uuid.UUID) -> list[Task]:
        """Reads all Task records by their user id"""
        tasks: list[Task] = session.query(Task).filter(Task.user_id == userId).all()
        return tasks
        