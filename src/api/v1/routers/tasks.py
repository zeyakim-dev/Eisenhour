from datetime import datetime

from fastapi import APIRouter, status

from src.models.task.schemas import TaskCreate, TaskInDB, TaskResponse

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate) -> TaskResponse:
    # TODO: Implement actual task creation logic
    # For now, return a dummy response
    dummy_task_in_db = TaskInDB(
        id=1,
        title=task.title,
        is_important=task.is_important,
        is_urgent=task.is_urgent,
        created_at=datetime.now(),
        completed_at=None,
        user_id=1,
        is_completed=False,
    )
    return TaskResponse.model_validate(dummy_task_in_db.model_dump())
