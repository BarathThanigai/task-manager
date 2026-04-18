from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import PaginatedTasks, TaskCreate, TaskRead, TaskUpdate
from app.services.auth import get_current_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


def _get_task_or_404(task_id: int, user_id: int, db: Session) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    task = Task(title=payload.title, description=payload.description, owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=PaginatedTasks)
def list_tasks(
    completed: bool | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PaginatedTasks:
    query = db.query(Task).filter(Task.owner_id == current_user.id)
    if completed is not None:
        query = query.filter(Task.completed == completed)

    total = query.count()
    tasks = query.order_by(Task.id.desc()).offset(skip).limit(limit).all()
    return PaginatedTasks(items=tasks, total=total, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    return _get_task_or_404(task_id, current_user.id, db)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    task = _get_task_or_404(task_id, current_user.id, db)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    task = _get_task_or_404(task_id, current_user.id, db)
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

