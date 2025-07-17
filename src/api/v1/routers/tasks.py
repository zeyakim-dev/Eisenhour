from collections.abc import AsyncGenerator
from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.db import SessionLocal
from src.models.task.models import Task
from src.models.task.schemas import TaskCreate, TaskResponse

router = APIRouter()


# Dependency to get the database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate, db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    new_task = Task(
        title=task.title,
        is_important=task.is_important,
        is_urgent=task.is_urgent,
        user_id=1,  # Placeholder for user_id, assuming a default user for now
        is_completed=False,
        created_at=datetime.now(),
        completed_at=None,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return TaskResponse.model_validate(new_task)


@router.get("/", response_model=list[TaskResponse])
async def get_all_tasks(db: AsyncSession = Depends(get_db)) -> list[TaskResponse]:
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return [TaskResponse.model_validate(task) for task in tasks]
