from .taskHelper import TaskHelper
from crud.task import TaskCRUD
from __init__ import getAsyncDbSession
import uuid
from models import Task

class TaskController(TaskHelper):

    def __init__(self, user):
        super().__init__(user)

    @getAsyncDbSession
    async def getAllTasks(self, session) -> list[Task]:
        """Gets all the tasks that belong to the authed user"""
        return TaskCRUD.readAllTasksByUserId(session=session, userId=self.user.id)

    @getAsyncDbSession
    async def createTask(self, session, title: str) -> Task:
        """Creates a task for the authed user"""    
        task = TaskCRUD.createTask(session, id=uuid.uuid4(), userId=self.user.id, title=title)
        return task

    @getAsyncDbSession
    async def updateTask(self, session, id: str, title: str) -> Task:
        """Updates a task for the authed user"""

        task = await self.getTask(session=session, id=uuid.UUID(id))
        task.title = title
        TaskCRUD.update(db=session)
        return task

    @getAsyncDbSession
    async def deleteTask(self, session, id: str) -> None:
        """Deletes a taks for the authed user"""
        task = await self.getTask(session=session, id=uuid.UUID(id))
        TaskCRUD.delete(db=session, model=task)
        return None