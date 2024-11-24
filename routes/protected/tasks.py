from fastapi import APIRouter
from routes.auth.main import userDepedency
from controllers.task.taskController import TaskController
from schemas.tasks import Task, CreateTaskRequest, UpdateTaskRequest
from starlette.responses import JSONResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/all", response_model=list[Task])
async def get_all_task(user: userDepedency):
    controller = TaskController(user=user)
    tasks = await controller.getAllTasks()
    return tasks

@router.post("/create", response_model=Task)
async def create_task(request: CreateTaskRequest, user: userDepedency):
    controller = TaskController(user=user)
    task = await controller.createTask(title=request.title)
    return task

@router.patch("/update/{task_id}", response_model=Task)
async def update_task(task_id: str, request: UpdateTaskRequest, user: userDepedency):
    controller = TaskController(user=user)
    task = await controller.updateTask(id=task_id, title=request.title)
    return task

@router.delete("/delete/{task_id}")
async def delete_task(task_id: str, user: userDepedency):
    controller = TaskController(user=user)
    await controller.deleteTask(id=task_id)
    content = {"detail":"Task deleted"}
    response = JSONResponse(content=content)
    return response