from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from repository.task_repository import TaskRepository
import schemas.tasks as schemas
from core.rate_limiter import limiter

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[schemas.Task])
@limiter.limit("30/minute")
def read_tasks(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return TaskRepository.get_tasks(db, skip, limit)


@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_task(request: Request, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return TaskRepository.create_task(db, task)


@router.put("/{task_id}", response_model=schemas.Task)
@limiter.limit("10/minute")
def update_task(request: Request, task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    result = TaskRepository.update_task(db, task_id, task)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    if not TaskRepository.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)