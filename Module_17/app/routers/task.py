from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import UpdateTask, CreateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/task', tags=['task'])

SessionDep = Annotated[Session, Depends(get_db)]

@router.get('/')
async def all_tasks(session: SessionDep):
    tasks = session.scalars(select(Task)).all()
    return tasks

@router.get('/task_id')
async def task_by_id(session: SessionDep, task_id: int):
    task = session.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    return task

@router.post('/create')
async  def create_task(session: SessionDep, user_id: int, create_task: CreateTask):
    user = session.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    session.execute(insert(Task).values(
        title=create_task.title,
        content=create_task.content,
        priority=create_task.priority,
        user_id=user_id,
        slug=slugify(create_task.title)))

    session.commit()
    return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put('/update')
async def update_task(session: SessionDep, task_id: int, update_task: UpdateTask):
    session.execute(update(Task).where(Task.id == task_id).values(
        title=update_task.title,
        content=update_task.content,
        priority=update_task.priority,
        slug=slugify(update_task.title)))

    session.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful'}

@router.delete('/delete')
async def delete_task(session: SessionDep, task_id: int):
    task = session.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )

    session.execute(delete(Task).where(Task.id == task_id))
    session.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful'
    }