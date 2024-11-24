from models import User
from crud.task import TaskCRUD
from errors import NotFoundError
import uuid

class TaskHelper:

    def __init__(self, user):
        self.__user: User = user
    
    @property
    def user(self) -> User:
        return self.__user
    
    async def getTask(self, session, id: uuid.UUID):
        """Get a specific task by it's id"""
    
        task = TaskCRUD.readTaskByIdandUserId(session=session, id=id, userId=self.user.id)

        if not task:
            raise NotFoundError("Task not found")
        
        return task