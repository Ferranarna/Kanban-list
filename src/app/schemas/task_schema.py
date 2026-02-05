import datetime
from pydantic import BaseModel, Field
from typing import Optional
from src.domain.entities.task import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    epic_id: int
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    target_date: Optional[datetime.datetime] = None
    finalization_criteria: Optional[str] = None
    finalization_date: Optional[datetime.datetime] = None
    status: TaskStatus = TaskStatus.TO_DO
    assignee: Optional[str] = None
    priority: TaskPriority = TaskPriority.LOW


class TaskResponse(BaseModel):
    id: int
    epic_id: int
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    target_date: Optional[datetime.datetime] = None
    finalization_criteria: Optional[str] = None
    finalization_date: Optional[datetime.datetime] = None
    status: TaskStatus = TaskStatus.TO_DO
    assignee: Optional[str] = None
    priority: TaskPriority = TaskPriority.LOW

    class Config:
        from_attributes = True # Esto permite que Pydantic lea la Entidad de Dominio